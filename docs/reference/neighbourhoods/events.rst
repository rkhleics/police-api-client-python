Events
======

.. currentmodule:: police_api.neighbourhoods

.. class:: Neighbourhood.Event(api, data={})

    A neighbourhood event (e.g. a beat meating or surgery).

    :param PoliceAPI api: The instance of ``PoliceAPI`` that is currently being
                          used.
    :param dict data: The attributes that will be copied to this instance.

    .. attribute:: neighbourhood

        :type: Neighbourhood

        The Neighbourhood Policing Team that organised this event.

    .. attribute:: title

        :type: str

        The title of the event.

    .. attribute:: type

        :type: str

        The type of the event.

    .. attribute:: description

        :type: str

        A description of the event.

    .. attribute:: contact_details

        :type: list

        A ``list`` of ``dict``, containing methods of contacting the event
        organisers.

        .. doctest::

            >>> event = neighbourhood.events[0]
            >>> pprint(event.contact_details)
            {u'twitter': u'http://www.twitter.com/CCLeicsPolice'}


    .. attribute:: start_date

        :type: list

        A ``list`` of ``dict``, containing methods of contacting the event
        organisers.

        .. doctest::

            >>> event = neighbourhood.events[0]
            >>> pprint(event.contact_details)
            {u'twitter': u'http://www.twitter.com/CCLeicsPolice'}


    .. attribute:: address

        :type: str

        The location of the event.

    .. attribute:: start_date

        :type: datetime.datetime

        The date and time that the event starts.

        .. doctest::

            >>> event = neighbourhood.events[0]
            >>> event.start_date
            datetime.datetime(2014, 7, 14, 9, 30)
