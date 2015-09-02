from .crime import NoLocationCrime, Crime, CrimeCategory
from .exceptions import InvalidCategoryException
from .forces import Force
from .neighbourhoods import Neighbourhood
from .service import BaseService, APIError
from .stop_and_search import Stop
from .utils import encode_polygon
from .version import __version__  # NOQA


class PoliceAPI(object):
    """
    .. doctest::

        >>> from police_api import PoliceAPI
        >>> api = PoliceAPI(user_agent='cops-and-robbers/9.9.9', timeout=60)

    :param base_url: The base endpoint URL for the Police API. Default:
                     ``'https://data.police.uk/api/'``
    :param user_agent: The user agent string to use. Default:
                       ``'police-api-client-python/<version>'``
    :param timeout: The timeout in seconds. Default: ``30``
    :param username: The username to authenticate with. Default: ``None``
    :param password: The password to authenticate with. Default: ``None``
    """

    def __init__(self, **config):
        self.service = BaseService(self, **config)
        self.crime_categories = {}

    def get_forces(self):
        """
        Get a list of all police forces. Uses the forces_ API call.

        .. _forces: https://data.police.uk/docs/method/forces/

        :rtype: list
        :return: A list of Force objects (one for each police force in England,
                 Wales and Northern Ireland).
        """

        forces = []
        for f in self.service.request('GET', 'forces'):
            forces.append(Force(self, id=f['id'], name=f['name']))
        return forces

    def get_force(self, id, **attrs):
        """
        Get an individual forces. Uses the force_ API call.

        .. _force: https://data.police.uk/docs/method/force/

        :param force: The force to get neighbourhoods for (either by ID or
                      Force object)
        :rtype: list
        :return: A list of Force objects (one for each police force in England,
                 Wales and Northern Ireland).
        """
        return Force(self, id=id, **attrs)

    def get_neighbourhoods(self, force):
        """
        Get a list of all neighbourhoods for a force. Uses the neighbourhoods_
        API call.

        .. _neighbourhoods: https://data.police.uk/docs/method/neighbourhoods/

        :param force: The force to get neighbourhoods for (either by ID or
                      Force object)
        :type force: str or Force
        :rtype: list
        :return: A ``list`` of Neighbourhood objects (one for each
                 Neighbourhood Policing Team in the given force).
        """

        if not isinstance(force, Force):
            force = Force(self, id=force)

        neighbourhoods = []
        for n in self.service.request('GET', '%s/neighbourhoods' % force.id):
            neighbourhoods.append(
                Neighbourhood(self, force=force, id=n['id'], name=n['name']))
        return sorted(neighbourhoods, key=lambda n: n.name)

    def get_neighbourhood(self, force, id, **attrs):
        """
        Get a specific neighbourhood. Uses the neighbourhood_ API call.

        .. _neighbourhood: https://data.police.uk/docs/method/neighbourhood/

        :param force: The force within which the neighbourhood resides (either
                      by ID or Force object)
        :type force: str or Force
        :param str neighbourhood: The ID of the neighbourhood to fetch.
        :rtype: Neighbourhood
        :return: The Neighbourhood object for the given force/ID.
        """

        if not isinstance(force, Force):
            force = Force(self, id=force, **attrs)

        return Neighbourhood(self, force=force, id=id, **attrs)

    def locate_neighbourhood(self, lat, lng):
        """
        Find a neighbourhood by location. Uses the locate-neighbourhood_ API
        call.

        .. _locate-neighbourhood:
            https://data.police.uk/docs/method/neighbourhood-locate/

        :param lat: The latitude of the location.
        :type lat: float or str
        :param lng: The longitude of the location.
        :type lng: float or str
        :rtype: Neighbourhood or None
        :return: The Neighbourhood object representing the Neighbourhood
                 Policing Team responsible for the given location.
         """

        method = 'locate-neighbourhood'
        q = '%s,%s' % (lat, lng)
        try:
            result = self.service.request('GET', method, q=q)
            return self.get_neighbourhood(result['force'],
                                          result['neighbourhood'])
        except APIError:
            pass

    def get_dates(self):
        """
        Get a list of available dates. Uses the crimes-street-dates_ API call.

        .. _crimes-street-dates:
            https://data.police.uk/docs/method/crimes-street-dates/

        :rtype: list
        :return: A ``list`` of ``str`` representing each monthly data set, in
                 the format ``YYYY-MM``, most recent first.
        """

        response = self.service.request('GET', 'crimes-street-dates')
        return [d['date'] for d in response]

    def get_latest_date(self):
        """
        Get the latest available date. Uses the crimes-street-dates_ API call
        (not crime-last-updated_, becuase the format differs).

        .. _crimes-street-dates:
            https://data.police.uk/docs/method/crimes-street-dates/
        .. _crime-last-updated:
            https://data.police.uk/docs/method/crime-last-updated/

        :rtype: str
        :return: The most recent data set's date, in the format ``YYYY-MM``.
        """

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
        """
        Get a list of crime categories, valid for a particular date. Uses the
        crime-categories_ API call.

        .. _crime-categories:
            https://data.police.uk/docs/method/crime-categories/

        :rtype: list
        :param date: The date of the crime categories to get.
        :type date: str or None
        :return: A ``list`` of crime categories which are valid at the
                 specified date (or at the latest date, if ``None``).
        """

        return sorted(self._get_crime_categories(date=date).values(),
                      key=lambda c: c.name)

    def get_crime_category(self, id, date=None):
        """
        Get a particular crime category by ID, valid at a particular date. Uses
        the crime-categories_ API call.

        :rtype: CrimeCategory
        :param str id: The ID of the crime category to get.
        :param date: The date that the given crime category is valid for (the
                     latest date is used if ``None``).
        :type date: str or None
        :return: A crime category with the given ID which is valid for the
                 specified date (or at the latest date, if ``None``).
        """

        try:
            return self._get_crime_categories(date=date)[id]
        except KeyError:
            raise InvalidCategoryException(
                'Category %s not found for %s' % (id, date))

    def get_crime(self, persistent_id):
        """
        Get a particular crime by persistent ID. Uses the outcomes-for-crime_
        API call.

        .. _outcomes-for-crime:
            https://data.police.uk/docs/method/outcomes-for-crime/

        :rtype: Crime
        :param str persistent_id: The persistent ID of the crime to get.
        :return: The ``Crime`` with the given persistent ID.
        """

        method = 'outcomes-for-crime/%s' % persistent_id
        response = self.service.request('GET', method)
        crime = Crime(self, data=response['crime'])
        crime._outcomes = []
        outcomes = response['outcomes']
        if outcomes is not None:
            for o in outcomes:
                o.update({
                    'crime': crime,
                })
                crime._outcomes.append(crime.Outcome(self, o))
        return crime

    def get_crimes_point(self, lat, lng, date=None, category=None):
        """
        Get crimes within a 1-mile radius of a location. Uses the crime-street_
        API call.

        .. _crime-street: https//data.police.uk/docs/method/crime-street/

        :rtype: list
        :param lat: The latitude of the location.
        :type lat: float or str
        :param lng: The longitude of the location.
        :type lng: float or str
        :param date: The month in which the crimes were reported in the format
                    ``YYYY-MM`` (the latest date is used if ``None``).
        :type date: str or None
        :param category: The category of the crimes to filter by (either by ID
                         or CrimeCategory object)
        :type category: str or CrimeCategory
        :return: A ``list`` of crimes which were reported within 1 mile of the
                 specified location, in the given month (optionally filtered by
                 category).
        """

        if isinstance(category, CrimeCategory):
            category = category.id
        method = 'crimes-street/%s' % (category or 'all-crime')
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

    def get_crimes_area(self, points, date=None, category=None):
        """
        Get crimes within a custom area. Uses the crime-street_ API call.

        .. _crime-street: https//data.police.uk/docs/method/crime-street/

        :rtype: list
        :param list points: A ``list`` of ``(lat, lng)`` tuples.
        :param date: The month in which the crimes were reported in the format
                    ``YYYY-MM`` (the latest date is used if ``None``).
        :type date: str or None
        :param category: The category of the crimes to filter by (either by ID
                         or CrimeCategory object)
        :type category: str or CrimeCategory
        :return: A ``list`` of crimes which were reported within the specified
                 boundary, in the given month (optionally filtered by
                 category).
        """

        if isinstance(category, CrimeCategory):
            category = category.id
        method = 'crimes-street/%s' % (category or 'all-crime')
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
        """
        Get crimes at a particular snap-point location. Uses the
        crimes-at-location_ API call.

        .. _crimes-at-location:
            https://data.police.uk/docs/method/crimes-at-location/

        :rtype: list
        :param int location_id: The ID of the location to get crimes for.
        :param date: The month in which the crimes were reported in the format
                    ``YYYY-MM`` (the latest date is used if ``None``).
        :type date: str or None
        :return: A ``list`` of crimes which were snapped to the location with
                 the specified ID in the given month.
        """

        kwargs = {
            'location_id': location_id,
        }
        crimes = []
        if date is not None:
            kwargs['date'] = date
        for c in self.service.request('GET', 'crimes-at-location', **kwargs):
            crimes.append(Crime(self, data=c))
        return crimes

    def get_crimes_no_location(self, force, date=None, category=None):
        """
        Get crimes with no location for a force. Uses the crimes-no-location_
        API call.

        .. _crimes-no-location:
            https://data.police.uk/docs/method/crimes-no-location/

        :rtype: list
        :param force: The force to get no-location crimes for.
        :type force: str or Force
        :param date: The month in which the crimes were reported in the format
                    ``YYYY-MM`` (the latest date is used if ``None``).
        :type date: str or None
        :param category: The category of the crimes to filter by (either by ID
                         or CrimeCategory object)
        :type category: str or CrimeCategory
        :return: A ``list`` of crimes which were reported in the given month,
                 by the specified force, but which don't have a location.
        """

        if not isinstance(force, Force):
            force = Force(self, id=force)

        if isinstance(category, CrimeCategory):
            category = category.id

        kwargs = {
            'force': force.id,
            'category': category or 'all-crime',
        }
        crimes = []
        if date is not None:
            kwargs['date'] = date
        for c in self.service.request('GET', 'crimes-no-location', **kwargs):
            crimes.append(NoLocationCrime(self, data=c))
        return crimes

    def get_stops_within_area(self, points, **kwargs):
        return [Stop(self, data) for data in self.service.request(
            'POST', 'stops-street', poly=encode_polygon(points), **kwargs)]

    def get_stops_within_radius(self, point, **kwargs):
        return [Stop(self, data) for data in self.service.request(
            'POST', 'stops-street', lat=point[0], lng=point[1], **kwargs)]

    def get_stops_location(self, location_id, **kwargs):
        return [Stop(self, data) for data in self.service.request(
            'POST', 'stops-at-location', location_id=location_id, **kwargs)]

    def get_stops_no_location(self, force, **kwargs):
        if not isinstance(force, Force):
            force = Force(self, id=force)

        return [Stop(self, data) for data in self.service.request(
            'GET', 'stops-no-location', force=force.id, **kwargs)]

    def get_stops_force(self, force, date=None, **kwargs):
        if not isinstance(force, Force):
            force = Force(self, id=force)

        return [Stop(self, data) for data in self.service.request(
            'GET', 'stops-force', force=force.id, date=date, **kwargs)]
