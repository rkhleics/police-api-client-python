import logging
import requests


logger = logging.getLogger(__name__)


class APIError(Exception):
    pass


class BaseService(object):

    def __init__(self, api, **config):
        self.api = api
        self.requester = requests.session()
        self.config = {
            'base_url': 'http://data.police.uk/api/',
        }
        self.config.update(config)
        self.set_credentials(self.config.get('username'),
                             self.config.get('password'))

    def set_credentials(self, username, password):
        if username and password:
            self.requester.auth = (username, password)

    def raise_for_status(self, request):
        try:
            request.raise_for_status()
        except requests.models.HTTPError as e:
            raise APIError(e)

    def request(self, verb, method, **kwargs):
        verb = verb.upper()
        request_kwargs = {
            'timeout': self.config.get('timeout', 20),
        }
        if verb == 'GET':
            request_kwargs['params'] = kwargs
        else:
            request_kwargs['data'] = kwargs
        url = self.config['base_url'] + method
        logger.debug('%s %s' % (verb, url))
        print url, request_kwargs.get('data')
        r = self.requester.request(verb, url, **request_kwargs)
        self.raise_for_status(r)
        return r.json()
