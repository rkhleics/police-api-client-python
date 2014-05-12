Police API
==========

.. currentmodule:: police_api

.. class:: PoliceAPI(**config)

    .. attribute:: service

        :type: BaseService

        The API service used to make requests for this client.

    .. method:: get_forces()

        :rtype: list
        :return: A list of Force objects (one for each police force in England,
                 Wales and Northern Ireland).

    .. method:: get_neighbourhoods(force)

        :param force: The force to get neighbourhoods for (either by ID or
                      Force object)
        :type force: str or Force
        :rtype: list
        :return: A list of Neighbourhood objects (one for each Neighbourhood
                 Policing Team in the given force).

    .. method:: get_neighbourhood(force, neighbourhood)

        :param force: The force within which the neighbourhood resides (either
                      by ID or Force object)
        :type force: str or Force
        :param str neighbourhood: The ID of the neighbourhood to fetch.
        :rtype: Neighbourhood
        :return: The Neighbourhood object for the given force/ID.

    .. method:: locate_neighbourhood(lat, lng)

        :param lat: The latitude of the location.
        :type lat: float or str
        :param lng: The longitude of the location.
        :type lng: float or str
        :rtype: Neighbourhood or None
        :return: The Neighbourhood object representing the Neighbourhood
                 Policing Team responsible for the given location.

    .. method:: get_dates()

        :rtype: list
        :return: A ``list`` of ``str`` representing each monthly data set, in
                 the format ``YYYY-MM``, most recent first.

    .. method:: get_latest_date()

        :rtype: str
        :return: The most recent data set's date, in the format ``YYYY-MM``.

    .. method:: get_crime_categories(date=None)

        :rtype: list
        :param date: The date of the crime categories to get.
        :type date: str or None
        :return: A ``list`` of crime categories which are valid at the
                 specified date (or at the latest date, if ``None``).

    .. method:: get_crime_category(id, date=None)

        :rtype: CrimeCategory
        :param str id: The ID of the crime category to get.
        :param date: The date that the given crime category is valid for (the
                     latest date is used if ``None``).
        :type date: str or None
        :return: A crime category with the given ID which is valid for the
                 specified date (or at the latest date, if ``None``).

    .. method:: get_crime(persistent_id)

        :rtype: Crime
        :param str persistent_id: The persistent ID of the crime to get.
        :return: The ``Crime`` with the given persistent ID.

    .. method:: get_crimes_point(lat, lng, date=None, category=None)

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

        :rtype: list
        :param int location_id: The ID of the location to get crimes for.
        :param date: The month in which the crimes were reported in the format
                    ``YYYY-MM`` (the latest date is used if ``None``).
        :type date: str or None
        :return: A ``list`` of crimes which were snapped to the location with
                 the specified ID in the given month.

    .. method:: get_crimes_no_location(force, date=None, category=None)

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
