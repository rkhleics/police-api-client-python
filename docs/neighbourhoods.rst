Neighbourhoods
==============

.. currentmodule:: police_api.neighbourhoods

.. class:: Neighbourhood(api, preload=False, **attrs)

    A Neighbourhood Policing Team.

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
        >>> 'City Centre Neighbourhood'

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
            >>> {"latitude": "52.6268", "longitude": "-1.12621"}

    .. attribute:: links

        :type: list

        A ``list`` of links relevant to this force.

        .. doctest::

            >>> neighbourhood.links
            >>> [{"title": "Leicester City Council", "url": "http://www.leicester.gov.uk/", "description": null}]

    .. attribute:: locations

        :type: list

        A ``list`` of police stations in this NPT.

        .. doctest::

            >>> neighbourhood.locations
            >>> [{"name": "Mansfield House", "longitude": null, "postcode": "LE1 3GG", "address": "74 Belgrave Gate\n, Leicester", "latitude": null, "type": "station", "description": null}]

    .. attribute:: contact_details

        :type: dict

        Ways that this NPT can be contacted.

        .. doctest::

            >>> neighbourhood.contact_details
            >>> {"twitter": "www.twitter.com/leicesterpolice", "facebook": "http://www.facebook.com/campuscops", "telephone": "101", "email": "central.lpu@leicestershire.pnn.police.uk"}
