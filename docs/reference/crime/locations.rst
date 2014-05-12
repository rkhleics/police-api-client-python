Locations
=========

.. currentmodule:: police_api.crime

.. class:: Location(api, data={})

    An anonymised location, to which crimes are "snapped".

    :param PoliceAPI api: The instance of ``PoliceAPI`` that is currently being
                          used.
    :param dict data: The attributes that will be copied to this instance.

    .. attribute:: id

        :type: int

        This location's unique ID.

    .. attribute:: name

        :type: str

        The name of this location (e.g. ``On or near Petrol Station``)

    .. attribute:: latitude

        :type: str

        This location's latitude.

    .. attribute:: longitude

        :type: str

        This location's longitude.

    .. attribute:: type

        :type: str

        This location's type (either ``Force`` or ``BTP``, indicating whether
        the location belongs to a police force or a railway station).

    .. method:: is_btp()

        :rtype: bool
        :return: ``True`` if this location's type is ``BTP``, and ``False``
                 otherwise.
