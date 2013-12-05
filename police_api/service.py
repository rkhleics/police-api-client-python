import logging
import requests

from .exceptions import APIError
from .version import __version__

logger = logging.getLogger(__name__)


class BaseService(object):

    def __init__(self, api, **config):
        self.api = api
        self.config = {
            'base_url': 'http://data.police.uk/api/',
            'user_agent': 'police-api-client-python/%s' % __version__,
        }
        self.config.update(config)

    def raise_for_status(self, request):
        try:
            request.raise_for_status()
        except requests.models.HTTPError as e:
            raise APIError(e)

    def _make_request(self, verb, url, params={}):
        request_kwargs = {
            'headers': {
                'User-Agent': self.config['user_agent'],
            },
            'timeout': self.config.get('timeout', 30),
        }
        if 'username' in self.config:
            request_kwargs['auth'] = (self.config.get('username', ''),
                                      self.config.get('password', ''))
        if verb == 'GET':
            request_kwargs['params'] = params
        else:
            request_kwargs['data'] = params
        logger.debug('%s %s' % (verb, url))
        r = requests.request(verb, url, **request_kwargs)
        self.raise_for_status(r)
        return r.json()

    def request(self, verb, method, **kwargs):
        url = self.config['base_url'] + method
        return self._make_request(verb.upper(), url, kwargs)
