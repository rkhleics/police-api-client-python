from .resource import Resource, api_request, APIError
from .forces import Force


class Neighbourhood(Resource):
    """
    A policing neighbourhood.
    """
    force = None
    _officers = None
    _events = None
    fields = ['contact_details', 'name', 'links', 'description', 'url_force',
              'population', 'centre', 'locations']

    class Officer(object):
        """
        A police officer.
        """
        neighbourhood = None
        fields = ['name', 'rank', 'contact_details', 'bio']

        def __init__(self, neighbourhood, data={}):
            self.neighbourhood = neighbourhood
            for field in self.fields:
                setattr(self, field, data.get(field))

    class Event(object):
        """
        A neighbourhood event.
        """
        neighbourhood = None
        fields = ['title', 'type', 'description', 'contact_details',
                  'start_date', 'address']

        def __init__(self, neighbourhood, data={}):
            self.neighbourhood = neighbourhood
            for field in self.fields:
                setattr(self, field, data.get(field))

    def __init__(self, force, id, name=None):
        self.force = force
        self.id = id
        if name:
            self.name = name
            self.fields = list(self.fields).remove('name')

    def __repr__(self):
        return '[%s] %s' % (self.force, self.id)

    def _get_api_method(self):
        return '%s/%s' % (self.force.slug, self.id)

    def _hydrate_population(self, data):
        return int(data)

    def _get_officers(self):
        officers = []
        method = '%s/%s/people' % (self.force.slug, self.id)
        for o in api_request(method):
            officers.append(self.Officer(neighbourhood=self, data=o))
        return officers

    def _get_events(self):
        events = []
        method = '%s/%s/events' % (self.force.slug, self.id)
        for e in api_request(method):
            events.append(self.Event(neighbourhood=self, data=e))
        return events

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


def get_neighbourhoods(force):
    if not isinstance(force, Force):
        force = Force(force)

    neighbourhoods = []
    for n in api_request('%s/neighbourhoods' % force.slug):
        neighbourhoods.append(
            Neighbourhood(force=force, id=n['id'], name=n['name']))
    return sorted(neighbourhoods, key=lambda n: n.name)


def locate_neighbourhood(lat, lng):
    method = 'locate-neighbourhood?q=%s,%s' % (lat, lng)
    try:
        result = api_request(method)
        return Neighbourhood(Force(result['force']), result['neighbourhood'])
    except APIError:
        pass
