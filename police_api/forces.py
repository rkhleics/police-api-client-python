from .neighbourhoods import Neighbourhood
from .resource import Resource, SimpleResource


class Force(Resource):
    """
    A police force.
    """
    id = None
    _resource_cache = {}
    _neighbourhoods = None
    fields = ['description', 'telephone', 'name', 'engagement_methods', 'url']

    class SeniorOfficer(SimpleResource):
        """
        A senior police officer.
        """
        fields = ['force', 'name', 'rank', 'contact_details', 'bio']

        def __str__(self):
            return '<Force.SeniorOfficer> %s' % self.name

    def __str__(self):
        return '<Force> %s' % self.name

    def _get_api_method(self):
        return 'forces/%s' % self.id

    def _get_resource(self, cls, method):
        if method in self._resource_cache:
            return self._resource_cache[method]
        objs = []
        method = 'forces/%s/%s' % (self.id, method)
        for d in self.api.service.request('GET', method):
            d.update({
                'force': self,
            })
            objs.append(cls(self.api, data=d))
        self._resource_cache[method] = objs
        return objs

    def get_neighbourhood(self, neighbourhood_id, **attrs):
        return Neighbourhood(self.api, force=self, id=neighbourhood_id,
                             **attrs)

    @property
    def senior_officers(self):
        return self._get_resource(self.SeniorOfficer, 'people')

    @property
    def neighbourhoods(self):
        if self._neighbourhoods is None:
            self._neighbourhoods = self.api.get_neighbourhoods(self)
        return self._neighbourhoods

    @property
    def slug(self):
        return self.id
