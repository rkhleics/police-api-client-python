Neighbourhoods
==============

.. toctree::

    events
    officers
    priorities

.. currentmodule:: police_api.neighbourhoods

.. class:: Neighbourhood(api, preload=False, **attrs)

    A Neighbourhood Policing Team. Uses the neighbourhood_ API call.

    :param PoliceAPI api: The instance of ``PoliceAPI`` that is currently being
                          used.
    :param bool preload: If ``True``, attributes are loaded from the API on
                         instantiation rather than waiting for a property to
                         be accessed.
    :param attrs: Only the ``force`` and ``id`` are required. Any other
                  attributes supplied will be set on the instance and not
                  fetched from the API.

    .. doctest::

        >>> from police_api import PoliceAPI
        >>> from police_api.forces import Force
        >>> from police_api.neighbourhoods import Neighbourhood
        >>> api = PoliceAPI()
        >>> force = Force(api, id='leicestershire')
        >>> neighbourhood = Neighbourhood(api, force=force, id='C04')
        >>> neighbourhood.name
        'City Centre Neighbourhood'

    .. attribute:: id

        :type: str

        The neighbourhood's identifier (usually a code, but can contain
        spaces).

    .. attribute:: name

        :type: str

        The name of the NPT.

    .. attribute:: description

        :type: str

        A description of the NPT's area.

    .. attribute:: url_force

        :type: str

        The URL for this NPT on the force's website

    .. attribute:: population

        :type: str

        An estimate of the number of people living within the NPT boundary.

    .. attribute:: centre

        :type: dict

        The approximate centre point of the neighbourhood.

        .. doctest::

            >>> neighbourhood.centre
            {"latitude": "52.6268", "longitude": "-1.12621"}

    .. attribute:: links

        :type: list

        A ``list`` of links relevant to this force.

        .. doctest::

            >>> pprint(neighbourhood.links)
            [{u'description': None,
              u'title': u'Leicester City Council',
              u'url': u'http://www.leicester.gov.uk/'},
             {u'description': None,
              u'title': u'Beaumont Leys LPU',
              u'url': u'http://leicspolice.wordpress.com/category/lpu-blogs/beaumont-leys/'}]

    .. attribute:: locations

        :type: list

        A ``list`` of police stations in this NPT.

        .. doctest::

            >>> pprint(neighbourhood.locations)
            [{u'address': u'2 Beaumont Way\n, Leicester',
              u'description': None,
              u'latitude': None,
              u'longitude': None,
              u'name': u'Beaumont Leys',
              u'postcode': u'LE4 1DS',
              u'type': u'station'}]

    .. attribute:: contact_details

        :type: dict

        Ways that this NPT can be contacted.

        .. doctest::

            >>> pprint(neighbourhood.contact_details)
            {u'email': u'beaumont.lpu@leicestershire.pnn.police.uk',
             u'facebook': u'http://www.facebook.com/leicestercitypolice',
             u'telephone': u'101',
             u'twitter': u'http://www.twitter.com/LPAbbey'}

    .. attribute:: officers

        :type: list

        A ``list`` of ``Neighbourhood.Officer`` objects.

    .. attribute:: events

        :type: list

        A ``list`` of ``Neighbourhood.Event`` objects.

    .. attribute:: priorities

        :type: list

        A ``list`` of ``Neighbourhood.Priority`` objects.

    .. attribute:: boundary

        :type: list

        A ``list`` of ``(lat, lng)`` coordinates representing the perimeter of
        this neighbourhood's boundary.

        .. doctest::

            >>> pprint(neighbourhood.boundary)
            [(52.6235790036, -1.1433951806),
             (52.6235759765, -1.1432002292),
             ...
             (52.6241719477, -1.143313233),
             (52.6235790036, -1.1433951806)]

.. _neighbourhood: http://data.police.uk/docs/method/neighbourhood/
