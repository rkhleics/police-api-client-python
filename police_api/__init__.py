from .crime import Crime, CrimeCategory
from .forces import Force
from .neighbourhoods import Neighbourhood
from .service import BaseService, APIError
from .utils import encode_polygon


class PoliceAPI(object):

    def __init__(self, **config):
        self.service = BaseService(self, **config)
        self.crime_categories = {}

    def get_forces(self):
        forces = []
        for f in self.service.request('GET', 'forces'):
            forces.append(Force(self, slug=f['id']))
        return forces

    def get_force(self, slug):
        return Force(self, slug=slug)

    def get_neighbourhoods(self, force):
        if not isinstance(force, Force):
            force = Force(self, slug=force)

        neighbourhoods = []
        for n in self.service.request('GET', '%s/neighbourhoods' % force.slug):
            neighbourhoods.append(
                Neighbourhood(self, force=force, id=n['id'], name=n['name']))
        return sorted(neighbourhoods, key=lambda n: n.name)

    def get_neighbourhood(self, force, id):
        if not isinstance(force, Force):
            force = Force(self, slug=force)

        return Neighbourhood(self, force=force, id=id)

    def locate_neighbourhood(self, lat, lng):
        method = 'locate-neighbourhood?q=%s,%s' % (lat, lng)
        try:
            result = self.service.request('GET', method)
            return self.get_neighbourhood(result['force'],
                                          result['neighbourhood'])
        except APIError:
            pass

    def get_dates(self):
        response = self.service.request('GET', 'crimes-street-dates')
        return [d['date'] for d in response]

    def get_latest_date(self):
        return self.service.request('GET', 'crime-last-updated')['date']

    def _populate_crime_categories(self):
        response = self.service.request('GET', 'crime-categories')
        for c in filter(lambda x: x['url'] != 'all-crime', response):
            self.crime_categories[c['url']] = CrimeCategory(self, data=c)

    def _get_crime_categories(self):
        if not self.crime_categories:
            self._populate_crime_categories()
        return self.crime_categories

    def get_crime_categories(self):
        return sorted(self._get_crime_categories().values(),
                      key=lambda c: c.name)

    def get_crime_category(self, url):
        return self._get_crime_categories()[url]

    def get_crimes_point(self, lat, lng, date=None):
        kwargs = {
            'lat': lat,
            'lng': lng,
        }
        crimes = []
        if date is not None:
            kwargs['date'] = date
        for c in self.service.request('GET', 'crimes-street/all-crime',
                                      **kwargs):
            crimes.append(Crime(self, data=c))
        return crimes

    def get_crimes_area(self, points, date=None):
        kwargs = {
            'poly': encode_polygon(points),
        }
        crimes = []
        if date is not None:
            kwargs['date'] = date
        for c in self.service.request('POST', 'crimes-street/all-crime',
                                      **kwargs):
            crimes.append(Crime(self, data=c))
        return crimes
