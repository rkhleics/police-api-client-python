Crime
=====

.. toctree::

    crime_categories
    outcome_categories
    locations
    outcomes

.. currentmodule:: police_api.crime

.. class:: Crime(api, data={})

    An individual crime. Uses the outcomes-for-crime_ API call.

    :param PoliceAPI api: The instance of ``PoliceAPI`` that is currently being
                          used.
    :param dict data: The attributes that will be copied to this instance.

    .. attribute:: id

        :type: int

        This crime's unique internal ID (not used elsewhere in the data or
        API).

    .. attribute:: persistent_id

        :type: str

        This crime's persistent ID, which is referenced by the outcomes data
        and in the CSV files. Not guaranteed to be unique.

    .. attribute:: month

        :type: str

        The month that this crime was reported in (``%m-%d``).

    .. attribute:: category

        :type: CrimeCategory

        The category of this crime.

    .. attribute:: location

        :type: Location

        The anonymised location that this crime occurred closest to.

    .. attribute:: context

        :type: str

        Additional data about this crime provided by the reporting force.

    .. attribute:: outcome_status

        :type: Crime.Outcome

        The latest outcome to have been recorded for this crime.

    .. attribute:: outcomes

        :type: list

        A ``list`` of ``Outcome`` objects for this crime.

.. _outcomes-for-crime: http://data.police.uk/docs/method/outcomes-for-crime/
