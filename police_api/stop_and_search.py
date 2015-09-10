from dateutil.parser import parse as parse_date

from .resource import SimpleResource
from .crime import Location


class Stop(SimpleResource):
    """
    A stop and search incident. Only a few of the attributes here are
    guaranteed to be provided by forces, so take care around any ``None``
    values you may see.

    .. doctest::

        >>> from police_api import PoliceAPI
        >>> api = PoliceAPI()
        >>> def sort_stops_by_date(unsorted_stops):
        ...     return(sorted(unsorted_stops, key=lambda s: s.datetime))
        >>> stops = sort_stops_by_date(
        ...     api.get_stops_force('metropolitan', '2015-07')
        ... )

    .. attribute:: age_range

        :type: str
        Human-readable string representing the age range of the person stopped.

        .. doctest::

            >>> print(stops[0].age_range)
            25-34

    .. attribute:: object_of_search

        :type: str
        The officer's justification for conducting the search.

        .. doctest::

            >>> print(stops[0].object_of_search)
            25-34

    .. attribute:: outcome

        :type: str
        The outcome of the stop.

        .. doctest::

            >>> print(stops[0].outcome)
            Offender given drugs possession warning

    .. attribute:: outcome_linked_to_object_of_search

        :type: bool
        Whether the outcome of the stop was related to the reason the stop was
        conducted.

    .. attribute:: legislation

        :type: str
        The legislation allowing this particular stop.

        .. doctest::

            >>> print(stops[0].legislation)
            Misuse of Drugs Act 1971 (section 23)

    .. attribute:: type

        :type: str
        What type of search this was (person, vehicle, etc.).

        .. doctest::

            >>> print(stops[0].type)
            Person search

    .. attribute:: involved_person

        :type: bool
        Whether or not a person was searched in this stop.

        .. doctest::

            >>> stops[0].involved_person
            True
            >>> vehicle_stop = [
            ...     s for s in stops if s.type == 'Vehicle search'
            ... ][0]
            >>> vehicle_stop.involved_person
            False

    .. attribute:: operation

        :type: bool
        Whether this stop was part of a policing operation.

    .. attribute:: operation_name

        :type: str
        The name of the policing operation this stop was part of, if
        applicable.

    .. attribute:: self_defined_ethnicity

        :type: str
        The ethnicity of the person stopped, as reported by the person stopped.

        .. doctest::

            >>> print(stops[0].self_defined_ethnicity)
            Black or Black British - Any other Black ethnic background (B9)

    .. attribute:: officer_defined_ethnicity

        :type: str
        The ethnicity of the person stopped, as reported by the officer who
        conducted the stop.

        .. doctest::

            >>> print(stops[0].officer_defined_ethnicity)
            Black

    .. attribute: gender

        :type: str
        The gender of the person stopped. It is not clear if this is as
        reported by the officer or the person stopped.

        .. doctest::

            >>> print(stops[0].gender)
            Male

    .. attribute: datetime

        :type: datetime
        When the stop was conducted. Note that if a force appears to only
        conduct stops at midnight, that probably means they don't record the
        time of stops.

        .. doctest::

            >>> print(stops[0].datetime.isoformat())
            2015-07-01T00:05:00

    .. attribute: location

        :type: :class:`Location`
        The approximate location of the stop.

    .. attribute: removal_of_more_than_outer_clothing

        :type: bool
        Whether significant clothing was removed in order to carry out the
        search.

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
