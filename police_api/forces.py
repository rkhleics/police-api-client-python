from .neighbourhoods import Neighbourhood
from .resource import Resource, SimpleResource


class Force(Resource):
    """
    A police force.

    .. doctest::

        >>> from police_api import PoliceAPI
        >>> from police_api.forces import Force
        >>> api = PoliceAPI()
        >>> force = Force(api, id='leicestershire')
        >>> force.name
        'Leicestershire'

    :param `PoliceAPI` api: The API instance to use.
    :param bool preload: If ``True``, attributes are loaded from the API on
                         instantiation rather than waiting for a property to
                         be accessed.
    :param attrs: Only the ``id`` is required. Any other attributes supplied
                  will be set on the instance and not fetched from the API.

    .. attribute:: id

        :type: str

        The force's identifier (a slugified version of the name).

    .. attribute:: name

        :type: str

        The full name of the force.

    .. attribute:: description

        :type: str

        A short description of the force's role.

    .. attribute:: url

        :type: str

        The force's website address.

    .. attribute:: telephone

        :type: str

        The force's main switchboard number. Usually set to ``'101'`` since the
        introduction of the national service.

    .. attribute:: engagement_methods

        :type: list

        A ``list`` of ``dict``, containing the keys ``url``, ``type``,
        ``description``, and ``title``.

        .. doctest::

            >>> pprint(force.engagement_methods)
            [{u'description': None,
              u'title': u'facebook',
              u'type': u'facebook',
              u'url': u'http://www.facebook.com/leicspolice'},
             {u'description': None,
              u'title': u'twitter',
              u'type': u'twitter',
              u'url': u'http://www.twitter.com/leicspolice'},
             {u'description': None,
              u'title': u'youtube',
              u'type': u'youtube',
              u'url': u'http://www.youtube.com/leicspolice'},
             {u'description': None,
              u'title': u'rss',
              u'type': u'rss',
              u'url': u'http://www.leics.police.uk/feeds/news/'},
             {u'description': None,
              u'title': u'telephone',
              u'type': u'telephone',
              u'url': u''},
             {u'description': None,
              u'title': u'flickr',
              u'type': u'flickr',
              u'url': u'http://www.flickr.com/photos/leicspolice-property'}]

    .. attribute:: neighbourhoods

        :type: list

        A ``list`` of ``Neighbourhood`` objects (all the Neighbourhood Policing
        Teams in this force area).

    .. attribute:: senior_officers

        :type: list

        A ``list`` of :class:`Force.SeniorOfficer` objects.
    """

    id = None
    _resource_cache = {}
    _neighbourhoods = None
    fields = ['description', 'telephone', 'name', 'engagement_methods', 'url']

    class SeniorOfficer(SimpleResource):
        """
        A senior police officer. Uses the senior-officers_ API call.

        :param `PoliceAPI` api: The API instance to use.
        :param dict data: The attributes that will be copied to this instance.

        .. attribute:: force

            :type: Force

            The police force that this officer works for.

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

                >>> officer = force.senior_officers[0]
                >>> pprint(officer.contact_details)
                {u'twitter': u'http://www.twitter.com/CCLeicsPolice'}

        .. _senior-officers:
            https://data.police.uk/docs/method/senior-officers/
        """
        fields = ['force', 'name', 'rank', 'contact_details', 'bio']

        def __str__(self):
            return '<Force.SeniorOfficer> %s' % self.name

    def __str__(self):
        return '<Force> %s' % self.name

    def _get_api_method(self):
        return 'forces/%s' % self.id

    def _get_resource(self, cls, method):
        if method in self._resource_cache:
            return self._resource_cache[method]
        objs = []
        method = 'forces/%s/%s' % (self.id, method)
        for d in self.api.service.request('GET', method):
            d.update({
                'force': self,
            })
            objs.append(cls(self.api, data=d))
        self._resource_cache[method] = objs
        return objs

    def get_neighbourhood(self, neighbourhood_id, **attrs):
        return Neighbourhood(self.api, force=self, id=neighbourhood_id,
                             **attrs)

    @property
    def senior_officers(self):
        return self._get_resource(self.SeniorOfficer, 'people')

    @property
    def neighbourhoods(self):
        if self._neighbourhoods is None:
            self._neighbourhoods = self.api.get_neighbourhoods(self)
        return self._neighbourhoods

    @property
    def slug(self):
        return self.id
