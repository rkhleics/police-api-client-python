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

    def request(self, verb, method, **kwargs):
        verb = verb.upper()
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
            request_kwargs['params'] = kwargs
        else:
            request_kwargs['data'] = kwargs
        url = self.config['base_url'] + method
        logger.debug('%s %s' % (verb, url))
        r = requests.request(verb, url, **request_kwargs)
        self.raise_for_status(r)
        return r.json()
