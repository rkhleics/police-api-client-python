Senior Officers
===============

.. currentmodule:: police_api.forces

.. class:: Force.SeniorOfficer(api, data={})

    A senior police officer.

    :param PoliceAPI api: The instance of ``PoliceAPI`` that is currently being
                          used.
    :param dict data: The attributes that will be copied to this instance.

    .. attribute:: force

        :type: Force

        The police force that this officer works for.

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

        .. doctest::

            >>> officer = force.senior_officers[0]
            >>> pprint(officer.contact_details)
            {u'twitter': u'http://www.twitter.com/CCLeicsPolice'}
