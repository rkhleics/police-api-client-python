from .resource import SimpleResource


class CrimeCategory(SimpleResource):
    """
    A crime category.
    """
    fields = ['url', 'name']

    def __str__(self):
        return '<CrimeCategory> %s' % self.name

    def __eq__(self, other):
        return isinstance(other, CrimeCategory) and self.url == other.url

    def __hash__(self):
        return hash(self.url)


class OutcomeCategory(SimpleResource):
    """
    An outcome category.
    """
    fields = ['code', 'name']

    def __str__(self):
        return '<OutcomeCategory> %s' % self.name

    def __eq__(self, other):
        return isinstance(other, OutcomeCategory) and self.code == other.code

    def __hash__(self):
        return hash(self.code)


class NoLocationCrime(SimpleResource):
    """
    A crime with no location.
    """
    fields = ['id', 'context', 'month']

    def _hydrate_category(self, url):
        return self.api.get_crime_category(url, date=self.month)

    def __str__(self):
        return '<NoLocationCrime> %s' % self.id


class Crime(NoLocationCrime):
    """
    A crime.
    """
    _outcomes = None
    fields = ['month', 'category', 'id', 'persistent_id', 'location',
              'location_type', 'location_subtype', 'context', 'outcome_status']

    class Outcome(SimpleResource):
        """
        An outcome for a specific crime.
        """
        crime = None
        fields = ['crime', 'category', 'date']

        def _hydrate_category(self, data):
            if not isinstance(data, dict):
                data = {
                    'name': data,
                }
            return OutcomeCategory(self.api, data)

        def __str__(self):
            return '<Crime.Outcome> %s' % self.category.name

    def _get_outcomes(self):
        outcomes = []
        method = 'outcomes-for-crime/%s' % self.persistent_id
        for o in self.api.request('GET', method)['outcomes']:
            o.update({
                'crime': self,
            })
            outcomes.append(self.Outcome(self.api, o))
        return outcomes

    @property
    def outcomes(self):
        if self._outcomes is None:
            self._outcomes = self._get_outcomes()
        return self._outcomes

    def _hydrate_location(self, data):
        return Location(self.api, data=data)

    def _hydrate_outcome_status(self, data):
        if data:
            data.update({
                'crime': self,
            })
            return self.Outcome(self.api, data)

    def _hydrate(self, data):
        data['location'].update({
            'type': data['location_type'],
            'subtype': data['location_subtype'],
        })
        return super(Crime, self)._hydrate(data)

    def __str__(self):
        return '<Crime> %s' % self.id


class Location(SimpleResource):
    """
    An anonymised location.
    """
    fields = ['latitude', 'longitude', 'street', 'type', 'subtype']

    def __init__(self, *args, **kwargs):
        super(Location, self).__init__(*args, **kwargs)

        # the 'street' dictionary contains the location's id and name
        self.id = self.street['id']
        self.name = self.street['name']

    def is_btp(self):
        return self.type == 'BTP'

    def __str__(self):
        return '<Location> %s' % self.id

    def __eq__(self, other):
        return isinstance(other, Location) and self.id == other.id

    def __hash__(self):
        return hash(self.id)
