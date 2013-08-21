from .resource import SimpleResource


class CrimeCategory(SimpleResource):
    """
    A crime category.
    """
    fields = ['url', 'name']

    def __str__(self):
        return '<CrimeCategory> %s' % self.name


class OutcomeCategory(SimpleResource):
    """
    An outcome category.
    """
    fields = ['code', 'name']

    def __str__(self):
        return '<OutcomeCategory> %s' % self.name


class Crime(SimpleResource):
    """
    A crime.
    """
    _outcomes = None
    fields = ['category', 'persistent_id', 'location', 'location_type',
              'location_subtype', 'id', 'context', 'month']

    class Outcome(SimpleResource):
        """
        An outcome for a specific crime.
        """
        crime = None
        fields = ['crime', 'category', 'date']

        def _hydrate_category(self, data):
            return OutcomeCategory(data)

        def __str__(self):
            return '<Crime.Outcome> %s' % self.category.name

    def _get_outcomes(self):
        outcomes = []
        method = 'outcomes-for-crime/%s' % self.persistent_id
        for o in self.api.request('GET', method)['outcomes']:
            o.update({
                'crime': self,
            })
            outcomes.append(self.Outcome(crime=self, data=o))
        return outcomes

    @property
    def outcomes(self):
        if self._outcomes is None:
            self._outcomes = self._get_outcomes()
        return self._outcomes

    def _hydrate_location(self, data):
        return Location(self.api, data=data)

    def _hydrate_category(self, url):
        return self.api.get_crime_category(url)

    def __str__(self):
        return '<Crime> %s' % self.id


class Location(SimpleResource):
    """
    An anonymised location.
    """
    fields = ['latitude', 'longitude', 'street']

    def __init__(self, *args, **kwargs):
        super(Location, self).__init__(*args, **kwargs)

        # the 'street' dictionary contains the location's id and name
        self.id = self.street['id']
        self.name = self.street['name']

    def __str__(self):
        return '<Location> %s' % self.id
