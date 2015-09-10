from .resource import SimpleResource


class CrimeCategory(SimpleResource):
    """
    A crime category. Uses the crime-categories_ API call.

    :param PoliceAPI api: The API instance to use.
    :param dict data: The attributes that will be copied to this instance.

    .. attribute:: id

        :type: str

        A slug representing this crime category.

    .. attribute:: name

        :type: str

        The name of this crime category.

    .. _crime-categories: https://data.police.uk/docs/method/crime-categories/
    """

    fields = ['id', 'url', 'name']

    def __init__(self, api, data={}):
        if data:
            data['id'] = data.get('url')
        super(CrimeCategory, self).__init__(api, data=data)

    def __str__(self):
        return '<CrimeCategory> %s' % self.name

    def __eq__(self, other):
        return isinstance(other, CrimeCategory) and self.id == other.id

    def __hash__(self):
        return hash(self.id)


class OutcomeCategory(SimpleResource):
    """
    An outcome category.

    :param PoliceAPI api: The API instance to use.
    :param dict data: The attributes that will be copied to this instance.

    .. attribute:: id

        :type: str

        A slug representing this outcome category.

    .. attribute:: name

        :type: str

        The name of this outcome category.
    """
    fields = ['id', 'code', 'name']

    def __init__(self, api, data={}):
        if data:
            data['id'] = data.get('code')
        super(OutcomeCategory, self).__init__(api, data=data)

    def __str__(self):
        return '<OutcomeCategory> %s' % self.name

    def __eq__(self, other):
        return isinstance(other, OutcomeCategory) and self.name == other.name

    def __hash__(self):
        return hash(self.name)


class NoLocationCrime(SimpleResource):
    """
    A crime with no location. Retrieved via the crimes-no-location_ API call.

    .. _crimes-no-location:
        https://data.police.uk/docs/method/crimes-no-location/
    """
    fields = ['id', 'context', 'month']

    def _hydrate_category(self, id):
        return self.api.get_crime_category(id, date=self.month)

    def __str__(self):
        return '<NoLocationCrime> %s' % self.id


class Crime(NoLocationCrime):
    """
    An individual crime. Uses the outcomes-for-crime_ API call.

    :param PoliceAPI api: The API instance to use.
    :param dict data: The attributes that will be copied to this instance.

    .. _outcomes-for-crime:
        https://data.police.uk/docs/method/outcomes-for-crime/

    .. attribute:: id

        :type: int

        This crime's unique internal ID (not used elsewhere in the data or
        API).

    .. attribute:: persistent_id

        :type: str

        This crime's persistent ID, which is referenced by the outcomes data
        and in the CSV files. Not guaranteed to be unique.

    .. attribute:: month

        :type: str

        The month that this crime was reported in (``%m-%d``).

    .. attribute:: category

        :type: :class:`CrimeCategory`

        The category of this crime.

    .. attribute:: location

        :type: :class:`Location`

        The anonymised location that this crime occurred closest to.

    .. attribute:: context

        :type: str

        Additional data about this crime provided by the reporting force.

    .. attribute:: outcome_status

        :type: :class:`Crime.Outcome`

        The latest outcome to have been recorded for this crime.

    .. attribute:: outcomes

        :type: list

        A ``list`` of :class:`Outcome` objects for this crime, in the order
        they occurred.
    """

    _outcomes = None
    fields = ['month', 'category', 'id', 'persistent_id', 'location',
              'location_type', 'location_subtype', 'context', 'outcome_status']

    class Outcome(SimpleResource):
        """
        An outcome for an individual crime.

        :param PoliceAPI api: The API instance to use.
        :param dict data: The attributes that will be copied to this instance.

        .. attribute:: crime

            :type: :class:`Crime`

            The crime that this outcome refers to.

        .. attribute:: category

            :type: :class:`OutcomeCategory`

            The category of this particular outcome.

        .. attribute:: date

            :type: str

            The month that this outcome was recorded in (``%m-%d``).
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

        if not self.persistent_id:
            return outcomes

        method = 'outcomes-for-crime/%s' % self.persistent_id
        for o in self.api.service.request('GET', method)['outcomes']:
            o.update({
                'crime': self,
            })
            outcomes.append(self.Outcome(self.api, o))

        if outcomes is None:
            return []
        else:
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
        if data['location']:
            data['location'].update({
                'type': data['location_type'],
                'subtype': data['location_subtype'],
            })
        return super(Crime, self)._hydrate(data)

    def __str__(self):
        return '<Crime> %s' % self.id


class Location(SimpleResource):
    """
    An anonymised location, to which crimes are "snapped". Information about
    how location anonymisation works is published on the `data.police.uk about
    page`_.

    .. _data.police.uk about page:
        https://data.police.uk/about/#location-anonymisation

    :param PoliceAPI api: The API instance to use.
    :param dict data: The attributes that will be copied to this instance.

    .. attribute:: id

        :type: int

        This location's unique ID.

    .. attribute:: name

        :type: str

        The name of this location (e.g. ``On or near Petrol Station``)

    .. attribute:: latitude

        :type: str

        This location's latitude.

    .. attribute:: longitude

        :type: str

        This location's longitude.

    .. attribute:: type

        :type: str

        This location's type (either ``'BTP'`` or ``'Force'``, indicating
        whether the location contains crimes snapped from the British Transport
        Police or all other forces).
    """
    fields = ['latitude', 'longitude', 'street', 'type', 'subtype']

    def __init__(self, *args, **kwargs):
        super(Location, self).__init__(*args, **kwargs)

        # the 'street' dictionary contains the location's id and name
        self.id = getattr(self, 'street', {}).get('id')
        self.name = getattr(self, 'street', {}).get('name')

    def is_btp(self):
        """
        :rtype: bool
        :return: ``True`` if this location's type is ``'BTP'``, and ``False``
                 otherwise.
        """
        return self.type == 'BTP'

    def __str__(self):
        return '<Location> %s' % self.id

    def __eq__(self, other):
        return isinstance(other, Location) and self.id == other.id

    def __hash__(self):
        return hash(self.id)
