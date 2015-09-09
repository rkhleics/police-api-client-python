from datetime import datetime

from .exceptions import NeighbourhoodsNeighbourhoodException
from .resource import Resource, SimpleResource


class Neighbourhood(Resource):
    """
    A Neighbourhood Policing Team. Uses the neighbourhood_ API call.

    :param PoliceAPI api: The instance of ``PoliceAPI`` to use.
    :param bool preload: If ``True``, attributes are loaded from the API on
                         instantiation rather than waiting for a property to
                         be accessed.
    :param attrs: Only the ``force`` and ``id`` are required. Any other
                  attributes supplied will be set on the instance and not
                  fetched from the API.

    .. doctest::

        >>> from police_api import PoliceAPI
        >>> api = PoliceAPI()
        >>> force = api.get_force('leicestershire')
        >>> neighbourhood = force.get_neighbourhood('C04')
        >>> print(neighbourhood.name)
        City Centre neighbourhood

    .. attribute:: id

        :type: str

        The neighbourhood's identifier (usually a code, but can contain
        spaces).

    .. attribute:: name

        :type: str

        The name of the NPT.

    .. attribute:: description

        :type: str

        A description of the NPT's area.

    .. attribute:: url_force

        :type: str

        The URL for this NPT on the force's website

    .. attribute:: population

        :type: str

        An estimate of the number of people living within the NPT boundary.

    .. attribute:: centre

        :type: dict

        The approximate centre point of the neighbourhood.

        .. doctest::

            >>> print(neighbourhood.centre['latitude'])
            52.6268
            >>> print(neighbourhood.centre['longitude'])
            -1.12621

    .. attribute:: links

        :type: list

        A ``list`` of links relevant to this force.

        .. doctest::

            >>> link = neighbourhood.links[0]
            >>> print(link['title'])
            Leicester City Council
            >>> print(link['url'])
            http://www.leicester.gov.uk/

    .. attribute:: locations

        :type: list

        A ``list`` of police stations in this NPT.

        .. doctest::

            >>> print(neighbourhood.locations[0]['address'])
            74 Belgrave Gate
            , Leicester

    .. attribute:: contact_details

        :type: dict

        Ways that this NPT can be contacted.

        .. doctest::

        >>> print(neighbourhood.contact_details['email'])
        centralleicester.npa@leicestershire.pnn.police.uk
        >>> print(neighbourhood.contact_details['twitter'])
        http://www.twitter.com/leicesterpolice

    .. attribute:: officers

        :type: list

        A ``list`` of ``Neighbourhood.Officer`` objects.

    .. attribute:: events

        :type: list

        A ``list`` of ``Neighbourhood.Event`` objects.

    .. attribute:: priorities

        :type: list

        A ``list`` of ``Neighbourhood.Priority`` objects.

    .. attribute:: boundary

        :type: list

        A ``list`` of ``(lat, lng)`` coordinates representing the perimeter of
        this neighbourhood's boundary.

        .. doctest::

            >>> neighbourhood.boundary[:2]
            [(52.6235790036, -1.1433951806), (52.6235759765, -1.1432002292)]

    .. _neighbourhood: https://data.police.uk/docs/method/neighbourhood/
    """
    force = None
    _resource_cache = {}
    _boundary = None
    _crimes = None
    fields = ['contact_details', 'name', 'links', 'description', 'url_force',
              'population', 'centre', 'locations']

    class Officer(SimpleResource):
        """
        A police officer. Uses the neighbourhood-team_ API call.

        :param PoliceAPI api: The instance of ``PoliceAPI`` to use.
        :param dict data: The attributes that will be copied to this instance.

        .. doctest::

            >>> from police_api import PoliceAPI
            >>> api = PoliceAPI()
            >>> force = api.get_force('surrey')
            >>> neighbourhood = force.get_neighbourhood('ELCO')
            >>> officer = neighbourhood.officers[0]

        .. attribute:: neighbourhood

            :type: :class:`Neighbourhood`

            The Neighbourhood Policing Team that this officer is part of.

        .. attribute:: name

            :type: str

            The officer's name.

        .. attribute:: rank

            :type: str

            The officer's rank.

        .. attribute:: bio

            :type: str

            The officer's biography.

        .. attribute:: contact_details

            :type: list

            A ``list`` of ``dict``, containing methods of contacting the
            officer.

            .. doctest::

                >>> print(officer.contact_details['email'])
                elmbridge@surrey.pnn.police.uk
                >>> print(officer.contact_details['telephone'])
                101

        .. _neighbourhood-team:
            https://data.police.uk/docs/method/neighbourhood-team/
        """
        fields = ['neighbourhood', 'name', 'rank', 'contact_details', 'bio']

        def __str__(self):
            return '<Neighbourhood.Officer> %s' % self.name

    class Event(SimpleResource):
        """
        A neighbourhood event (e.g. a beat meating or surgery). Uses the
        neighbourhood-events_ API call.

        :param PoliceAPI api: The instance of ``PoliceAPI`` to use.
        :param dict data: The attributes that will be copied to this instance.

        .. doctest::

            >>> from police_api import PoliceAPI
            >>> api = PoliceAPI()
            >>> force = api.get_force('leicestershire')
            >>> neighbourhood = force.get_neighbourhood('C04')
            >>> event = neighbourhood.events[0]

        .. attribute:: neighbourhood

            :type: :class:`Neighbourhood`

            The Neighbourhood Policing Team that organised this event.

        .. attribute:: title

            :type: str

            The title of the event.

        .. attribute:: type

            :type: str

            The type of the event.

        .. attribute:: description

            :type: str

            A description of the event.

        .. attribute:: address

            :type: str

            The location of the event.

        .. attribute:: start_date

            :type: datetime.datetime

            The date and time that the event starts.

        .. _neighbourhood-events:
            https://data.police.uk/docs/method/neighbourhood-events/
        """

        fields = ['neighbourhood', 'title', 'type', 'description',
                  'contact_details', 'start_date', 'address']

        def __str__(self):
            return '<Neighbourhood.Event> %s' % self.title

        def _hydrate_start_date(self, data):
            return datetime.strptime(data, '%Y-%m-%dT%H:%M:%S')

    class Priority(SimpleResource):
        """
        A neighbourhood priority (i.e. an issue raised by the community and
        a corresponding policing action to address this). Uses the
        neighbourhood-priorities_ API call.

        :param PoliceAPI api: The instance of ``PoliceAPI`` to use.
        :param dict data: The attributes that will be copied to this instance.

        .. attribute:: neighbourhood

            :type: :class:`Neighbourhood`

            The Neighbourhood Policing Team that owns this priority.

        .. attribute:: issue

            :type: str

            The issue that was raised.

        .. attribute:: action

            :type: str

            The action that was taken to address the issue.

        .. attribute:: issue_date

            :type: datetime.datetime

            The date that the issue was raised.

        .. attribute:: action_date

            :type: datetime.datetime

            The date that the action was implemented.

        .. _neighbourhood-priorities:
            https://data.police.uk/docs/method/neighbourhood-priorities/
        """

        fields = ['neighbourhood', 'issue', 'action', 'issue_date',
                  'action_date']

        def __str__(self):
            return '<Neighbourhood.Priority> %s' % self.issue

        def _hydrate(self, data):
            for field in ['issue-date', 'action-date']:
                data[field.replace('-', '_')] = data[field]
            return super(Neighbourhood.Priority, self)._hydrate(data)

        def __hydrate_date(self, data):
            return datetime.strptime(data, '%Y-%m-%dT%H:%M:%S')

        def _hydrate_issue_date(self, data):
            return self.__hydrate_date(data) if data else None

        _hydrate_action_date = _hydrate_issue_date

    def __init__(self, *args, **kwargs):
        super(Neighbourhood, self).__init__(*args, **kwargs)
        self._assert_id_not_neighbourhoods()

    def __str__(self):
        return '<Neighbourhood> %s' % self.id

    def __eq__(self, other):
        return isinstance(other, Neighbourhood) and self.id == other.id

    def __hash__(self):
        return hash(self.id)

    def _assert_id_not_neighbourhoods(self):
        # Have a look at the docstring of NeighbourhoodsNeighbourhoodException.
        if self.id == 'neighbourhoods':
            raise NeighbourhoodsNeighbourhoodException()

    def _get_api_method(self):
        self._assert_id_not_neighbourhoods()
        return '%s/%s' % (self.force.id, self.id)

    def _hydrate_population(self, data):
        return int(data) if data is not None else None

    def _get_resource(self, cls, method):
        if method in self._resource_cache:
            return self._resource_cache[method]
        objs = []
        method = '%s/%s/%s' % (self.force.id, self.id, method)
        for d in self.api.service.request('GET', method):
            d.update({
                'neighbourhood': self,
            })
            objs.append(cls(self.api, data=d))
        self._resource_cache[method] = objs
        return objs

    def _get_boundary(self):
        method = '%s/%s/boundary' % (self.force.id, self.id)
        points = self.api.service.request('GET', method)
        return [(float(p['latitude']), float(p['longitude'])) for p in points]

    def _get_crimes(self):
        return self.api.get_crimes_area(self.boundary)

    @property
    def officers(self):
        return self._get_resource(self.Officer, 'people')

    @property
    def events(self):
        return self._get_resource(self.Event, 'events')

    @property
    def priorities(self):
        return sorted(self._get_resource(self.Priority, 'priorities'),
                      key=lambda x: x.issue_date, reverse=True)

    @property
    def boundary(self):
        if self._boundary is None:
            self._boundary = self._get_boundary()
        return self._boundary

    @property
    def crimes(self):
        if self._crimes is None:
            self._crimes = self._get_crimes()
        return self._crimes
