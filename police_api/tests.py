import datetime
import json
import responses
from unittest import TestCase

from . import PoliceAPI
from .exceptions import NeighbourhoodsNeighbourhoodException


class PoliceAPITestCase(TestCase):
    api = PoliceAPI()

    def run(self, *args, **kwargs):
        @responses.activate
        def wrapped():
            return super(PoliceAPITestCase, self).run(*args, **kwargs)
        return wrapped()


class TestForces(PoliceAPITestCase):

    def test_forces_empty(self):
        responses.add(responses.GET, 'https://data.police.uk/api/forces',
                      body='[]', content_type='application/json')
        forces = self.api.get_forces()
        self.assertEqual(len(forces), 0)

    def test_forces_single(self):
        responses.add(responses.GET, 'https://data.police.uk/api/forces',
                      body='[{"id": "test-force", "name": "Test Force"}]',
                      content_type='application/json')
        forces = self.api.get_forces()
        self.assertEqual(len(forces), 1)
        self.assertEqual(forces[0].id, 'test-force')
        self.assertEqual(forces[0].name, 'Test Force')


class TestForce(PoliceAPITestCase):

    def test_force_slug_equals_id(self):
        force = self.api.get_force(id='test-force')
        self.assertEqual(force.slug, 'test-force')

    def test_force_attribute_access(self):
        attributes = {
            'name': 'Test Force',
            'description': 'A test force',
            'telephone': '01234 567890',
            'url': 'http://test-force.com',
            'engagement_methods': [
                {
                    'url': 'http://www.facebook.com/pages/test-page',
                    'description': 'Test Facebook page',
                    'title': 'Facebook',
                },
                {
                    'url': 'http://www.twitter.com/test',
                    'description': 'Test Twitter page',
                    'title': 'Twitter'
                },
            ],
        }
        responses.add(responses.GET,
                      'https://data.police.uk/api/forces/test-force',
                      body=json.dumps(attributes),
                      content_type='application/json')

        force = self.api.get_force(id='test-force')

        for key, val in attributes.items():
            self.assertEqual(getattr(force, key), val)

    def test_force_senior_officers(self):
        people = [
            {
                'name': 'Test Officer',
                'rank': 'Chief Constable',
                'bio': 'A test officer',
            },
        ]
        responses.add(
            responses.GET,
            'https://data.police.uk/api/forces/test-force/people',
            body=json.dumps(people), content_type='application/json')
        force = self.api.get_force(id='test-force')
        self.assertEqual(len(force.senior_officers), 1)
        self.assertEqual(force.senior_officers[0].name, 'Test Officer')
        self.assertEqual(force.senior_officers[0].rank, 'Chief Constable')
        self.assertEqual(force.senior_officers[0].bio, 'A test officer')

    def test_force_neighbourhoods_empty(self):
        responses.add(responses.GET,
                      'https://data.police.uk/api/test-force/neighbourhoods',
                      body='[]', content_type='application/json')
        force = self.api.get_force(id='test-force')
        self.assertEqual(len(force.neighbourhoods), 0)

    def test_force_neighbourhoods_single(self):
        neighbourhood = {
            'id': 'test-neighbourhood',
            'name': 'Test Neighbourhood',
        }
        neighbourhoods = [neighbourhood]
        responses.add(
            responses.GET,
            'https://data.police.uk/api/test-force/neighbourhoods',
            body=json.dumps(neighbourhoods),
            content_type='application/json')
        responses.add(
            responses.GET,
            'https://data.police.uk/api/test-force/test-neighbourhood',
            body=json.dumps(neighbourhood),
            content_type='application/json')
        force = self.api.get_force(id='test-force')
        self.assertEqual(len(force.neighbourhoods), 1)
        self.assertEqual(force.neighbourhoods[0].id, 'test-neighbourhood')
        self.assertEqual(force.neighbourhoods[0].name, 'Test Neighbourhood')
        self.assertEqual(force.get_neighbourhood('test-neighbourhood').name,
                         'Test Neighbourhood')


class TestNeighbourhood(PoliceAPITestCase):

    def test_neighbourhood_empty(self):
        responses.add(responses.GET,
                      'https://data.police.uk/api/test-force/neighbourhoods',
                      body='[]', content_type='application/json')
        neighbourhoods = self.api.get_neighbourhoods('test-force')
        self.assertEqual(len(neighbourhoods), 0)

    def test_neighbourhood_single(self):
        neighbourhoods = [
            {
                'id': 'test-neighbourhood',
                'name': 'Test Neighbourhood',
            },
        ]
        responses.add(responses.GET,
                      'https://data.police.uk/api/test-force/neighbourhoods',
                      body=json.dumps(neighbourhoods),
                      content_type='application/json')
        neighbourhoods = self.api.get_neighbourhoods('test-force')
        self.assertEqual(len(neighbourhoods), 1)
        self.assertEqual(neighbourhoods[0].id, 'test-neighbourhood')
        self.assertEqual(neighbourhoods[0].name, 'Test Neighbourhood')

    def test_neighbourhood_population(self):
        attributes = {
            'population': '27000',
        }
        responses.add(
            responses.GET,
            'https://data.police.uk/api/test-force/test-neighbourhood',
            body=json.dumps(attributes), content_type='application/json')
        neighbourhood = self.api.get_neighbourhood(
            'test-force', 'test-neighbourhood')
        self.assertEqual(type(neighbourhood.population), int)
        self.assertEqual(neighbourhood.population, 27000)

    def test_neighbourhood_officers(self):
        people = [
            {
                'name': 'Test Officer',
                'rank': 'PC',
                'bio': 'A test officer',
            },
        ]
        responses.add(
            responses.GET,
            'https://data.police.uk/api/test-force/test-neighbourhood/people',
            body=json.dumps(people), content_type='application/json')
        neighbourhood = self.api.get_neighbourhood(
            'test-force', 'test-neighbourhood')
        self.assertEqual(len(neighbourhood.officers), 1)
        self.assertEqual(neighbourhood.officers[0].name, 'Test Officer')
        self.assertEqual(neighbourhood.officers[0].rank, 'PC')
        self.assertEqual(neighbourhood.officers[0].bio, 'A test officer')

    def test_neighbourhood_events(self):
        events = [
            {
                'title': 'Test Event',
                'description': 'A test event',
                'address': '123 Fake Street, Test Town',
                'start_date': '2010-01-01T09:00:00',
            },
        ]
        responses.add(
            responses.GET,
            'https://data.police.uk/api/test-force/test-neighbourhood/events',
            body=json.dumps(events), content_type='application/json')
        neighbourhood = self.api.get_neighbourhood(
            'test-force', 'test-neighbourhood')
        self.assertEqual(len(neighbourhood.events), 1)
        self.assertEqual(neighbourhood.events[0].title, 'Test Event')
        self.assertEqual(neighbourhood.events[0].description, 'A test event')
        self.assertEqual(neighbourhood.events[0].address,
                         '123 Fake Street, Test Town')
        self.assertEqual(type(neighbourhood.events[0].start_date),
                         datetime.datetime)
        self.assertEqual(neighbourhood.events[0].start_date,
                         datetime.datetime(year=2010, month=1, day=1, hour=9))

    def test_neighbourhood_priorities(self):
        priorities = [
            {
                'issue': 'Test issue',
                'action': 'Test action',
                'issue-date': '2010-01-01T00:00:00',
                'action-date': '2010-01-01T00:00:00',
            },
        ]
        responses.add(
            responses.GET,
            ('https://data.police.uk/api/test-force/test-neighbourhood/'
             'priorities'),
            body=json.dumps(priorities), content_type='application/json')
        neighbourhood = self.api.get_neighbourhood(
            'test-force', 'test-neighbourhood')
        self.assertEqual(len(neighbourhood.priorities), 1)
        self.assertEqual(neighbourhood.priorities[0].issue, 'Test issue')
        self.assertEqual(neighbourhood.priorities[0].action, 'Test action')
        self.assertEqual(type(neighbourhood.priorities[0].issue_date),
                         datetime.datetime)
        self.assertEqual(neighbourhood.priorities[0].issue_date,
                         datetime.datetime(year=2010, month=1, day=1))
        self.assertEqual(type(neighbourhood.priorities[0].action_date),
                         datetime.datetime)
        self.assertEqual(neighbourhood.priorities[0].action_date,
                         datetime.datetime(year=2010, month=1, day=1))

    def test_neighbourhood_priorities_sorting(self):
        priorities = [
            {
                'issue': 'Test issue 2',
                'action': None,
                'issue-date': '2010-02-01T00:00:00',
                'action-date': None,
            },
            {
                'issue': 'Test issue 3',
                'action': None,
                'issue-date': '2010-03-01T00:00:00',
                'action-date': None,
            },
            {
                'issue': 'Test issue 1',
                'action': None,
                'issue-date': '2010-01-01T00:00:00',
                'action-date': None,
            },
        ]
        responses.add(
            responses.GET,
            'https://data.police.uk/api/test-force/test-neighbourhood/'
            'priorities',
            body=json.dumps(priorities), content_type='application/json')
        neighbourhood = self.api.get_neighbourhood(
            'test-force', 'test-neighbourhood')
        self.assertEqual(len(neighbourhood.priorities), 3)
        issues = [p.issue for p in neighbourhood.priorities]
        self.assertEqual(
            issues,
            ['Test issue 3', 'Test issue 2', 'Test issue 1'])

    def test_neighbourhood_boundary(self):
        boundary = [
            {
                'latitude': '52.6235790036',
                'longitude': '-1.1433951806'
            },
            {
                'latitude': '52.6235719827',
                'longitude': '-1.142946221'
            },
            {
                'latitude': '52.6229371188',
                'longitude': '-1.1429732023'
            },
            {
                'latitude': '52.6220381746',
                'longitude': '-1.1424250637'
            },
        ]
        responses.add(
            responses.GET,
            'https://data.police.uk/api/test-force/test-neighbourhood/'
            'boundary',
            body=json.dumps(boundary), content_type='application/json')
        neighbourhood = self.api.get_neighbourhood(
            'test-force', 'test-neighbourhood')
        self.assertEqual(len(neighbourhood.boundary), 4)
        self.assertEqual(neighbourhood.boundary, [
            (52.6235790036, -1.1433951806),
            (52.6235719827, -1.142946221),
            (52.6229371188, -1.1429732023),
            (52.6220381746, -1.1424250637),
        ])

    def test_neighbourhood_neighbourhoods(self):
        """
        Ensure attempting to get a resource relating the the 'neighbourhoods'
        neighbourhood raises an NeighbourhoodsNeighbourhoodException exception.
        """

        self.assertRaises(
            NeighbourhoodsNeighbourhoodException,
            lambda: self.api.get_neighbourhood('test-force', 'neighbourhoods')
        )

        responses.add(
            responses.GET,
            'https://data.police.uk/api/forces/test-force',
            body='{}', content_type='application/json')

        self.assertRaises(
            NeighbourhoodsNeighbourhoodException,
            lambda: self.api.get_neighbourhood('test-force', 'neighbourhoods',
                                               preload=True)
        )

        self.assertRaises(
            NeighbourhoodsNeighbourhoodException,
            lambda: self.api.get_force('test-force').get_neighbourhood(
                'neighbourhoods')
        )

        floating_neighbourhood = self.api.get_neighbourhood('test', 'test')
        floating_neighbourhood.id = 'neighbourhoods'
        self.assertRaises(
            NeighbourhoodsNeighbourhoodException,
            lambda: floating_neighbourhood.name
        )


class TestLocateNeighbourhood(PoliceAPITestCase):

    def test_locate_neighbourhood_not_found(self):
        responses.add(responses.GET,
                      'https://data.police.uk/api/locate-neighbourhood',
                      status=404, content_type='application/json')
        neighbourhood = self.api.locate_neighbourhood(52.5, -0.05)
        self.assertEqual(neighbourhood, None)

    def test_locate_neighbourhood_found(self):
        result = {
            'force': 'leicestershire',
            'neighbourhood': 'C04'
        }
        responses.add(responses.GET,
                      'https://data.police.uk/api/locate-neighbourhood',
                      body=json.dumps(result), content_type='application/json')
        neighbourhood = self.api.locate_neighbourhood(52.5, -0.05)
        self.assertEqual(neighbourhood.id, 'C04')
        self.assertEqual(neighbourhood.force.id, 'leicestershire')
        self.assertEqual(neighbourhood,
                         self.api.get_neighbourhood('leicestershire', 'C04'))


class TestDates(PoliceAPITestCase):

    def test_get_dates(self):
        dates = [
            {'date': '2013-10'},
            {'date': '2013-09'},
            {'date': '2013-08'},
        ]
        responses.add(responses.GET,
                      'https://data.police.uk/api/crimes-street-dates',
                      body=json.dumps(dates), content_type='application/json')
        crime_dates = self.api.get_dates()
        self.assertEqual(len(crime_dates), 3)
        self.assertEqual(crime_dates, ['2013-10', '2013-09', '2013-08'])

    def test_get_latest_date(self):
        dates = [
            {'date': '2013-10'},
            {'date': '2013-09'},
            {'date': '2013-08'},
        ]
        responses.add(responses.GET,
                      'https://data.police.uk/api/crimes-street-dates',
                      body=json.dumps(dates), content_type='application/json')
        latest_date = self.api.get_latest_date()
        self.assertEqual(latest_date, '2013-10')


class TestStops(PoliceAPITestCase):
    def test_get_stops(self):
        result = [{
            'removal_of_more_than_outer_clothing': None,
            'datetime': '2015-04-01T17:30:00',
            'legislation': 'Misuse of Drugs Act 1971 (section 23)',
            'outcome': 'Suspect summonsed to court',
            'location': {
                'latitude': '51.284396',
                'longitude': '-2.495092',
                'street': {
                    'id': 535912,
                    'name': 'On or near Longvernal'
                }
            },
            'operation': None,
            'self_defined_ethnicity': 'White - White British (W1)',
            'type': 'Person and Vehicle search',
            'age_range': '25-34',
            'gender': 'Male',
            'operation_name': None,
            'outcome_linked_to_object_of_search': None,
            'object_of_search': 'Controlled drugs',
            'involved_person': True,
            'officer_defined_ethnicity': 'White'
        }, {
            'location': {
                'latitude': '51.456751',
                'longitude': '-2.589860',
                'street': {
                    'name': 'On or near Shopping Area',
                    'id': 543525
                }
            },
            'self_defined_ethnicity': 'White - White British (W1)',
            'operation': None,
            'type': 'Person search',
            'age_range': '10-17',
            'gender': 'Female',
            'operation_name': None,
            'outcome_linked_to_object_of_search': None,
            'object_of_search': 'Stolen goods',
            'involved_person': True,
            'officer_defined_ethnicity': 'White',
            'removal_of_more_than_outer_clothing': None,
            'legislation': 'Police and Criminal Evidence Act 1984 (section 1)',
            'datetime': '2015-04-01T18:00:00',
            'outcome': 'Local resolution'
        }]

        responses.add(responses.GET,
                      'https://data.police.uk/api/stops-force',
                      body=json.dumps(result), content_type='application/json')

        self.assertEqual([
            s.age_range for s in
            self.api.get_stops_force('metropolitan')
        ], [d['age_range'] for d in result])
