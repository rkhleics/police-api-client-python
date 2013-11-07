from datetime import datetime

from .resource import Resource, SimpleResource


class Neighbourhood(Resource):
    """
    A policing neighbourhood.
    """
    force = None
    _resource_cache = {}
    _boundary = None
    _crimes = None
    fields = ['contact_details', 'name', 'links', 'description', 'url_force',
              'population', 'centre', 'locations']

    class Officer(SimpleResource):
        """
        A police officer.
        """
        fields = ['neighbourhood', 'name', 'rank', 'contact_details', 'bio']

        def __str__(self):
            return '<Neighbourhood.Officer> %s' % self.name

    class Event(SimpleResource):
        """
        A neighbourhood event.
        """
        fields = ['neighbourhood', 'title', 'type', 'description',
                  'contact_details', 'start_date', 'address']

        def __str__(self):
            return '<Neighbourhood.Event> %s' % self.title

        def _hydrate_start_date(self, data):
            return datetime.strptime(data, '%Y-%m-%dT%H:%M:%S')

    class Priority(SimpleResource):
        """
        A neighbourhood priority.
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

    def __str__(self):
        return '<Neighbourhood> %s' % self.id

    def _get_api_method(self):
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
