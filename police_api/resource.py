import requests

API_URL = 'http://data.police.uk/api/'


class APIError(Exception):
    pass


def api_request(method):
    r = requests.get(API_URL + method)
    if r.status_code != 200:
        raise APIError(r.status_code)
    return r.json()


class Resource(object):
    _requested = False
    api_method = None
    fields = []

    def __getattr__(self, attr):
        if not self._requested and attr in self.fields:
            self._make_api_request()
        return self.__getattribute__(attr)

    def _make_api_request(self):
        self._response_data = api_request(self._get_api_method())
        self._hydrate()
        self._requested = True

    def _get_api_method(self):
        if self.api_method is None:
            raise RuntimeError('You must set the api_method attribute')
        return self.api_method

    def _hydrate(self):
        for field in self.fields:
            hydrate_field = getattr(self, '_hydrate_%s' % field, lambda x: x)
            setattr(self, field, hydrate_field(self._response_data.get(field)))
