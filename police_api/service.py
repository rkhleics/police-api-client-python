import logging
import requests

from .exceptions import APIError
from .version import __version__

logger = logging.getLogger(__name__)


class BaseService(object):
    session = None

    def __init__(self, api, **config):
        self.api = api
        self.config = {
            'base_url': 'http://data.police.uk/api/',
            'user_agent': 'police-api-client-python/%s' % __version__,
        }
        self.config.update(config)

    def get_session(self):
        if self.session is None:
            self.session = requests.session()
            self.session.auth = (self.config.get('username'),
                                 self.config.get('password'))
        return self.session

    def __del__(self):
        if self.session is not None:
            self.session.close()

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
        if verb == 'GET':
            request_kwargs['params'] = kwargs
        else:
            request_kwargs['data'] = kwargs
        url = self.config['base_url'] + method
        logger.debug('%s %s' % (verb, url))
        r = self.get_session().request(verb, url, **request_kwargs)
        r.connection.close()
        self.raise_for_status(r)
        return r.json()
