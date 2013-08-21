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

    def request(self, verb, method, **kwargs):
        verb = verb.upper()
        request_kwargs = {}
        if method == 'GET':
            request_kwargs['params'] = kwargs
        else:
            request_kwargs['data'] = kwargs
        url = self.config['base_url'] + method
        logger.debug('%s %s' % (verb, url))
        r = self.requester.request(verb, url, **request_kwargs)
        if r.status_code != 200:
            with open('/tmp/resp.html', 'w') as f:
                f.write(r.content)
            raise APIError(r.status_code)
        return r.json()
