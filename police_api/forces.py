from .resource import Resource


class Force(Resource):
    """
    A police force.
    """
    slug = None
    _neighbourhoods = None
    fields = ['description', 'telephone', 'name', 'engagement_methods', 'url']

    def __str__(self):
        return '<Force> %s' % self.name

    def _get_api_method(self):
        return 'forces/%s' % self.slug

    @property
    def neighbourhoods(self):
        if self._neighbourhoods is None:
            self._neighbourhoods = self.api.get_neighbourhoods(self)
        return self._neighbourhoods
