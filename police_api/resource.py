class SimpleResource(object):

    def __init__(self, api, data={}):
        self.api = api
        if data:
            self._hydrate(data)

    def _hydrate(self, data):
        for field in self.fields:
            hydrate_field = getattr(self, '_hydrate_%s' % field, lambda x: x)
            setattr(self, field, hydrate_field(data.get(field)))

    def __repr__(self):
        return self.__str__()


class Resource(SimpleResource):
    _requested = False
    api_method = None
    fields = []

    def __init__(self, api, preload=False, **attrs):
        super(Resource, self).__init__(api)
        for key, val in attrs.items():
            setattr(self, key, val)
            if key in self.fields:
                self.fields = list(self.fields)
                self.fields.remove(key)
        if preload:
            self._make_api_request()

    def __getattr__(self, attr):
        if not self._requested and attr in self.fields:
            self._make_api_request()
        return self.__getattribute__(attr)

    def _make_api_request(self):
        self._response_data = self.api.service.request(
            'GET', self._get_api_method())
        self._hydrate(self._response_data)
        self._requested = True

    def _get_api_method(self):
        if self.api_method is None:
            raise RuntimeError('You must set the api_method attribute')
        return self.api_method
