Forces
======

.. toctree::

    senior_officers

.. currentmodule:: police_api.forces

.. class:: Force(api, preload=False, **attrs)

    A police force in England, Wales or Northern Ireland. Uses the force_ API
    call.

    .. doctest::

        >>> from police_api import PoliceAPI
        >>> from police_api.forces import Force
        >>> api = PoliceAPI()
        >>> force = Force(api, id='leicestershire')
        >>> force.name
        'Leicestershire'

    :param PoliceAPI api: The instance of ``PoliceAPI`` that is currently being
                          used.
    :param bool preload: If ``True``, attributes are loaded from the API on
                         instantiation rather than waiting for a property to
                         be accessed.
    :param attrs: Only the ``id`` is required. Any other attributes supplied
                  will be set on the instance and not fetched from the API.

    .. attribute:: id

        :type: str

        The force's identifier (a slugified version of the name).

    .. attribute:: name

        :type: str

        The full name of the force.

    .. attribute:: description

        :type: str

        A short description of the force's role.

    .. attribute:: url

        :type: str

        The force's website address.

    .. attribute:: telephone

        :type: str

        The force's main switchboard number. Usually set to ``'101'`` since the
        introduction of the national service.

    .. attribute:: engagement_methods

        :type: list

        A ``list`` of ``dict``, containing the keys ``url``, ``type``,
        ``description``, and ``title``.

        .. doctest::

            >>> pprint(force.engagement_methods)
            [{u'description': None,
              u'title': u'facebook',
              u'type': u'facebook',
              u'url': u'http://www.facebook.com/leicspolice'},
             {u'description': None,
              u'title': u'twitter',
              u'type': u'twitter',
              u'url': u'http://www.twitter.com/leicspolice'},
             {u'description': None,
              u'title': u'youtube',
              u'type': u'youtube',
              u'url': u'http://www.youtube.com/leicspolice'},
             {u'description': None,
              u'title': u'rss',
              u'type': u'rss',
              u'url': u'http://www.leics.police.uk/feeds/news/'},
             {u'description': None,
              u'title': u'telephone',
              u'type': u'telephone',
              u'url': u''},
             {u'description': None,
              u'title': u'flickr',
              u'type': u'flickr',
              u'url': u'http://www.flickr.com/photos/leicspolice-property'}]

    .. attribute:: neighbourhoods

        :type: list

        A ``list`` of ``Neighbourhood`` objects (all the Neighbourhood Policing
        Teams in this force area).

    .. attribute:: senior_officers

        :type: list

        A ``list`` of ``Force.SeniorOfficer`` objects.

.. _force: http://data.police.uk/docs/method/force/
