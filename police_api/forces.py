from .resource import Resource, api_request


class Force(Resource):
    """
    A police force.
    """
    slug = None
    _neighbourhoods = None
    fields = ['description', 'telephone', 'name', 'engagement_methods']

    def __init__(self, slug):
        self.slug = slug

    def __repr__(self):
        return self.slug

    def _get_api_method(self):
        return 'forces/%s' % self.slug

    @property
    def neighbourhoods(self):
        if self._neighbourhoods is None:
            self._neighbourhoods = get_neighbourhoods(self)
        return self._neighbourhoods


def get_forces():
    forces = []
    for f in api_request('forces'):
        forces.append(Force(slug=f['id']))
    return forces
