Crime Categories
================

.. currentmodule:: police_api.crime

.. class:: CrimeCategory(api, data={})

    A crime category.

    :param PoliceAPI api: The instance of ``PoliceAPI`` that is currently being
                          used.
    :param dict data: The attributes that will be copied to this instance.

    .. attribute:: id

        :type: str

        This crime category's slugified name.

    .. attribute:: name

        :type: str

        The name of this crime category.
