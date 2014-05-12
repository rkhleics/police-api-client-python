Forces
======

.. currentmodule:: police_api.forces

.. class:: Force(api, preload=False, **attrs)

    A police force.

    .. doctest::

        >>> from police_api import PoliceAPI
        >>> from police_api.forces import Force
        >>> api = PoliceAPI()
        >>> force = Force(api, id='leicestershire')
        >>> force.name
        >>> 'Leicestershire'

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

    .. attribute:: neighbourhoods

        :type: list

        A ``list`` of ``Neighbourhood`` objects (all the Neighbourhood Policing
        Teams in this force area).

    .. attribute:: senior_officers

        :type: list

        A ``list`` of ``Force.SeniorOfficer`` objects.


.. class:: Force.SeniorOfficer(api, data={})

    A senior police officer.

    :param PoliceAPI api: The instance of ``PoliceAPI`` that is currently being
                          used.
    :param dict data: The attributes that will be copied to this instance.

    .. attribute:: force

        :type: str

        The force's identifier (a slugified version of the name).
        fields = ['force', 'name', 'rank', 'contact_details', 'bio']

    .. attribute:: name

        :type: str

        The officer's name.

    .. attribute:: rank

        :type: str

        The officer's rank.

    .. attribute:: bio

        :type: str

        The officer's biography.

    .. attribute:: contact_details

        :type: list

        A ``list`` of ``dict``, containing methods of contacting the officer.
