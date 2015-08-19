from dateutil.parser import parse as parse_date

from .resource import SimpleResource
from .crime import Location


class Stop(SimpleResource):
    """
    A Stop and Search incident.
    """

    fields = [
        'age_range', 'outcome', 'legislation', 'type', 'operation',
        'operation_name', 'self_defined_ethnicity', 'gender', 'datetime',
        'outcome_linked_to_object_of_search', 'location', 'involved_person',
        'removal_of_more_than_outer_clothing', 'officer_defined_ethnicity',
        'object_of_search',
    ]

    def __str__(self):
        return '<Stop> at %s' % self.datetime

    def _hydrate_location(self, data):
        return Location(self.api, data=data)

    def _hydrate_datetime(self, data):
        if data:
            return parse_date(data)
