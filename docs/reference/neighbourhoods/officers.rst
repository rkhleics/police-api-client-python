Officers
========

.. currentmodule:: police_api.neighbourhoods

.. class:: Neighbourhood.Officer(api, data={})

    A police officer. Uses the neighbourhood-team_ API call.

    :param PoliceAPI api: The instance of ``PoliceAPI`` to use.
    :param dict data: The attributes that will be copied to this instance.

    .. attribute:: neighbourhood

        :type: Neighbourhood

        The Neighbourhood Policing Team that this officer has responsibility
        for.

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

            >>> officer = neighbourhood.officers[0]
            >>> pprint(officer.contact_details)
            {u'telephone': u'01788 853851',
             u'website': u'http://www.safer-neighbourhoods.co.uk/your-neighbourhood/rugby-district/rugby-rural-south/email-the-team'}

.. _neighbourhood-team: http://data.police.uk/docs/method/neighbourhood-team/
