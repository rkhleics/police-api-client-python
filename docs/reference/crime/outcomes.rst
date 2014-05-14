Outcomes
========

.. currentmodule:: police_api.crime

.. class:: Crime.Outcome(api, data={})

    An outcome for an individual crime.

    :param PoliceAPI api: The instance of ``PoliceAPI`` to use.
    :param dict data: The attributes that will be copied to this instance.

    .. attribute:: crime

        :type: Crime

        The crime that this outcome refers to.

    .. attribute:: category

        :type: OutcomeCategory

        The category of this particular outcome.

    .. attribute:: date

        :type: str

        The month that this outcome was recorded in (``%m-%d``).
