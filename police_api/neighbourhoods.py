from .resource import Resource, SimpleResource


class Neighbourhood(Resource):
    """
    A policing neighbourhood.
    """
    force = None
    _officers = None
    _events = None
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

    def __str__(self):
        return '<Neighbourhood> %s' % self.id

    def _get_api_method(self):
        return '%s/%s' % (self.force.slug, self.id)

    def _hydrate_population(self, data):
        return int(data) if data is not None else None

    def _get_officers(self):
        officers = []
        method = '%s/%s/people' % (self.force.slug, self.id)
        for o in self.api.service.request('GET', method):
            o.update({
                'neighbourhood': self,
            })
            officers.append(self.Officer(self.api, data=o))
        return officers

    def _get_events(self):
        events = []
        method = '%s/%s/events' % (self.force.slug, self.id)
        for e in self.api.service.request('GET', method):
            e.update({
                'neighbourhood': self,
            })
            events.append(self.Event(self.api, data=e))
        return events

    def _get_boundary(self):
        method = '%s/%s/boundary' % (self.force.slug, self.id)
        points = self.api.service.request('GET', method)
        return [(float(p['latitude']), float(p['longitude'])) for p in points]

    def _get_crimes(self):
        return self.api.get_crimes_area(self.boundary)

    @property
    def officers(self):
        if self._officers is None:
            self._officers = self._get_officers()
        return self._officers

    @property
    def events(self):
        if self._events is None:
            self._events = self._get_events()
        return self._events

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
