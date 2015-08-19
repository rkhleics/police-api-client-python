Crime Categories
================

.. currentmodule:: police_api.crime

.. class:: CrimeCategory(api, data={})

    A crime category. Uses the crime-categories_ API call.

    :param PoliceAPI api: The instance of ``PoliceAPI`` to use.
    :param dict data: The attributes that will be copied to this instance.

    .. attribute:: id

        :type: str

        This crime category's slugified name.

    .. attribute:: name

        :type: str

        The name of this crime category.

.. _crime-categories: https://data.police.uk/docs/method/crime-categories/
