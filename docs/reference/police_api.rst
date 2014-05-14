Police API
==========

.. currentmodule:: police_api

.. class:: PoliceAPI(**config)

    .. doctest::

        >>> from police_api import PoliceAPI
        >>> api = PoliceAPI(user_agent='cops-and-robbers/9.9.9', timeout=60)

    :param base_url: The base endpoint URL for the Police API. Default:
                     ``'http://data.police.uk/api/'``
    :param user_agent: The user agent string to use. Default:
                       ``'police-api-client-python/<version>'``
    :param timeout: The timeout in seconds. Default: ``30``
    :param username: The username to authenticate with. Default: ``None``
    :param password: The password to authenticate with. Default: ``None``

    .. method:: get_forces()

        Get a list of all police forces. Uses the forces_ API call.

        :rtype: list
        :return: A list of Force objects (one for each police force in England,
                 Wales and Northern Ireland).

    .. method:: get_neighbourhoods(force)

        Get a list of all neighbourhoods for a force. Uses the neighbourhoods_
        API call.

        :param force: The force to get neighbourhoods for (either by ID or
                      Force object)
        :type force: str or Force
        :rtype: list
        :return: A ``list`` of Neighbourhood objects (one for each
                 Neighbourhood Policing Team in the given force).

    .. method:: get_neighbourhood(force, neighbourhood)

        Get a specific neighbourhood. Uses the neighbourhood_ API call.

        :param force: The force within which the neighbourhood resides (either
                      by ID or Force object)
        :type force: str or Force
        :param str neighbourhood: The ID of the neighbourhood to fetch.
        :rtype: Neighbourhood
        :return: The Neighbourhood object for the given force/ID.

    .. method:: locate_neighbourhood(lat, lng)

        Find a neighbourhood by location. Uses the locate-neighbourhood_ API
        call.

        :param lat: The latitude of the location.
        :type lat: float or str
        :param lng: The longitude of the location.
        :type lng: float or str
        :rtype: Neighbourhood or None
        :return: The Neighbourhood object representing the Neighbourhood
                 Policing Team responsible for the given location.

    .. method:: get_dates()

        Get a list of available dates. Uses the crimes-street-dates_ API call.

        :rtype: list
        :return: A ``list`` of ``str`` representing each monthly data set, in
                 the format ``YYYY-MM``, most recent first.

    .. method:: get_latest_date()

        Get the latest available date. Uses the crimes-street-dates_ API call
        (not crime-last-updated_, becuase the format differs).

        :rtype: str
        :return: The most recent data set's date, in the format ``YYYY-MM``.

    .. method:: get_crime_categories(date=None)

        Get a list of crime categories, valid for a particular date. Uses the
        crime-categories_ API call.

        :rtype: list
        :param date: The date of the crime categories to get.
        :type date: str or None
        :return: A ``list`` of crime categories which are valid at the
                 specified date (or at the latest date, if ``None``).

    .. method:: get_crime_category(id, date=None)

        Get a particular crime category by ID, valid at a particular date. Uses
        the crime-categories_ API call.

        :rtype: CrimeCategory
        :param str id: The ID of the crime category to get.
        :param date: The date that the given crime category is valid for (the
                     latest date is used if ``None``).
        :type date: str or None
        :return: A crime category with the given ID which is valid for the
                 specified date (or at the latest date, if ``None``).

    .. method:: get_crime(persistent_id)

        Get a particular crime by persistent ID. Uses the outcomes-for-crime_
        API call.

        :rtype: Crime
        :param str persistent_id: The persistent ID of the crime to get.
        :return: The ``Crime`` with the given persistent ID.

    .. method:: get_crimes_point(lat, lng, date=None, category=None)

        Get crimes within a 1-mile radius of a location. Uses the crime-street_
        API call.

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

    .. method:: get_crimes_area(points, date=None, category=None)

        Get crimes within a custom area. Uses the crime-street_ API call.

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

    .. method:: get_crimes_location(location_id, date=None)

        Get crimes at a particular snap-point location. Uses the
        crimes-at-location_ API call.

        :rtype: list
        :param int location_id: The ID of the location to get crimes for.
        :param date: The month in which the crimes were reported in the format
                    ``YYYY-MM`` (the latest date is used if ``None``).
        :type date: str or None
        :return: A ``list`` of crimes which were snapped to the location with
                 the specified ID in the given month.

    .. method:: get_crimes_no_location(force, date=None, category=None)

        Get crimes with no location for a force. Uses the crimes-no-location_
        API call.

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

.. _forces: http://data.police.uk/docs/method/forces/
.. _neighbourhoods: http://data.police.uk/docs/method/neighbourhoods/
.. _neighbourhood: http://data.police.uk/docs/method/neighbourhood/
.. _locate-neighbourhood: http://data.police.uk/docs/method/neighbourhood-locate/
.. _crimes-street-dates: http://data.police.uk/docs/method/crimes-street-dates/
.. _crime-last-updated: http://data.police.uk/docs/method/crime-last-updated/
.. _crime-categories: http://data.police.uk/docs/method/crime-categories/
.. _outcomes-for-crime: http://data.police.uk/docs/method/outcomes-for-crime/
.. _crime-street: http://data.police.uk/docs/method/crime-street/
.. _crimes-at-location: http://data.police.uk/docs/method/crimes-at-location/
.. _crimes-no-location: http://data.police.uk/docs/method/crimes-no-location/
