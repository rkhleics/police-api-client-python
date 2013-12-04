import json
import responses
from unittest import TestCase

from . import PoliceAPI


class PoliceAPITestCase(TestCase):
    api = PoliceAPI()

    def run(self, *args, **kwargs):
        @responses.activate
        def wrapped():
            return super(PoliceAPITestCase, self).run(*args, **kwargs)
        return wrapped()


class TestForces(PoliceAPITestCase):

    def test_forces_empty(self):
        responses.add(responses.GET, 'http://data.police.uk/api/forces',
                      body='[]', content_type='application/json')
        forces = self.api.get_forces()
        self.assertEqual(len(forces), 0)

    def test_forces_single(self):
        responses.add(responses.GET, 'http://data.police.uk/api/forces',
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
                      'http://data.police.uk/api/forces/test-force',
                      body=json.dumps(attributes),
                      content_type='application/json')

        force = self.api.get_force(id='test-force')

        for key, val in attributes.items():
            self.assertEqual(getattr(force, key), val)

    def test_force_neighbourhoods_empty(self):
        responses.add(responses.GET,
                      'http://data.police.uk/api/test-force/neighbourhoods',
                      body='[]', content_type='application/json')
        force = self.api.get_force(id='test-force')
        self.assertEqual(len(force.neighbourhoods), 0)

    def test_force_neighbourhoods_single(self):
        neighbourhoods = [
            {
                'id': 'test-neighbourhood',
                'name': 'Test Neighbourhood',
            },
        ]
        responses.add(responses.GET,
                      'http://data.police.uk/api/test-force/neighbourhoods',
                      body=json.dumps(neighbourhoods),
                      content_type='application/json')
        force = self.api.get_force(id='test-force')
        self.assertEqual(len(force.neighbourhoods), 1)
        self.assertEqual(force.neighbourhoods[0].id, 'test-neighbourhood')
        self.assertEqual(force.neighbourhoods[0].name, 'Test Neighbourhood')


class TestNeighbourhoods(PoliceAPITestCase):

    def test_neighbourhoods_empty(self):
        responses.add(responses.GET,
                      'http://data.police.uk/api/test-force/neighbourhoods',
                      body='[]', content_type='application/json')
        neighbourhoods = self.api.get_neighbourhoods('test-force')
        self.assertEqual(len(neighbourhoods), 0)

    def test_neighbourhoods_single(self):
        neighbourhoods = [
            {
                'id': 'test-neighbourhood',
                'name': 'Test Neighbourhood',
            },
        ]
        responses.add(responses.GET,
                      'http://data.police.uk/api/test-force/neighbourhoods',
                      body=json.dumps(neighbourhoods),
                      content_type='application/json')
        neighbourhoods = self.api.get_neighbourhoods('test-force')
        self.assertEqual(len(neighbourhoods), 1)
        self.assertEqual(neighbourhoods[0].id, 'test-neighbourhood')
        self.assertEqual(neighbourhoods[0].name, 'Test Neighbourhood')
