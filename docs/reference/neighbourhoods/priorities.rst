Priorities
==========

.. currentmodule:: police_api.neighbourhoods

.. class:: Neighbourhood.Priority(api, data={})

    A neighbourhood priority (i.e. an issue raised by the community and
    a corresponding policing action to address this). Uses the
    neighbourhood-priorities_ API call.

    :param PoliceAPI api: The instance of ``PoliceAPI`` to use.
    :param dict data: The attributes that will be copied to this instance.

    .. attribute:: neighbourhood

        :type: Neighbourhood

        The Neighbourhood Policing Team that owns this priority.

    .. attribute:: issue

        :type: str

        The issue that was raised.

    .. attribute:: action

        :type: str

        The action that was taken to address the issue.

    .. attribute:: issue_date

        :type: datetime.datetime

        The date that the issue was raised.

    .. attribute:: action_date

        :type: datetime.datetime

        The date that the action was implemented.

.. _neighbourhood-priorities: https://data.police.uk/docs/method/neighbourhood-priorities/
