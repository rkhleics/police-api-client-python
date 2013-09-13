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
        return self.get_dates()[0]

    def _populate_crime_categories(self, date=None):
        response = self.service.request('GET', 'crime-categories', date=date)
        self.crime_categories[date] = {}
        for c in filter(lambda x: x['url'] != 'all-crime', response):
            self.crime_categories[date][c['url']] = CrimeCategory(self, data=c)

    def _get_crime_categories(self, date=None):
        if date not in self.crime_categories:
            self._populate_crime_categories(date=date)
        return self.crime_categories[date]

    def get_crime_categories(self, date=None):
        return sorted(self._get_crime_categories(date=date).values(),
                      key=lambda c: c.name)

    def get_crime_category(self, url, date=None):
        return self._get_crime_categories(date=date)[url]

    def get_crime(self, persistent_id):
        method = 'outcomes-for-crime/%s' % persistent_id
        response = self.service.request('GET', method)
        crime = Crime(self, data=response['crime'])
        crime._outcomes = []
        for o in response['outcomes']:
            o.update({
                'crime': crime,
            })
            crime._outcomes.append(crime.Outcome(self, o))
        return crime

    def get_crimes_point(self, lat, lng, date=None, category='all-crime'):
        if isinstance(category, CrimeCategory):
            category = category.url
        method = 'crimes-street/%s' % category
        kwargs = {
            'lat': lat,
            'lng': lng,
        }
        crimes = []
        if date is not None:
            kwargs['date'] = date
        for c in self.service.request('GET', method, **kwargs):
            crimes.append(Crime(self, data=c))
        return crimes

    def get_crimes_area(self, points, date=None, category='all-crime'):
        if isinstance(category, CrimeCategory):
            category = category.url
        method = 'crimes-street/%s' % category
        kwargs = {
            'poly': encode_polygon(points),
        }
        crimes = []
        if date is not None:
            kwargs['date'] = date
        for c in self.service.request('POST', method, **kwargs):
            crimes.append(Crime(self, data=c))
        return crimes

    def get_crimes_location(self, location_id, date=None):
        kwargs = {
            'location_id': location_id,
        }
        crimes = []
        if date is not None:
            kwargs['date'] = date
        for c in self.service.request('GET', 'crimes-at-location', **kwargs):
            crimes.append(Crime(self, data=c))
        return crimes
