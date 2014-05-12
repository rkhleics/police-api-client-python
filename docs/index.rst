Police API Client (Python)
==========================

The Police API Client is an open-source client for the `Police API`_. It was
built to power the new Police.uk_ website.

View the README_ for installation instructions and quick-start examples.


Configuration
-------------

The API doesn't require any configuration or authentication to get going, but
you can provide credentials if you have them::

    >>> from police_api import PoliceAPI
    >>> api = PoliceAPI(username='weroc42', password='abc123')


Dates
-----

The data is updated monthly, and each data set is represented by a date string,
in the format ``YYYY-MM``. For example::

    >>> from police_api import PoliceAPI
    >>> api = PoliceAPI()
    >>> api.get_dates()
    [u'2013-10', u'2013-09', u'2013-08', ..., u'2010-12']
    >>> api.get_latest_date()
    u'2013-10'

This can then be used to filter the crimes by date::

    >>> api.get_crimes_point(52.63473, -1.137514, date='2013-08')
    [<Crime> 26926242, ..., <Crime> 26925710]


Forces
------

To retrieve a list of police forces, use ``get_forces()``::

    >>> api.get_forces()
    [<Force> Avon and Somerset Constabulary, ..., <Force> Wiltshire Police]

If you know the ID of a particular force, then you can use ``get_force()``::

    >>> force = api.get_force('leicestershire')
    >>> force
    <Force> Leicestershire Police


Neighbourhoods
--------------

Forces are broken down into *Neighbourhood Policing Teams*::

    >>> force.neighbourhoods
    [<Neighbourhood> C02, <Neighbourhood> L03, ..., <Neighbourhood> L69]

If you know the ID of a particular neighbourhood, then you can use
``get_neighbourhood()``::

    >>> neighbourhood = api.get_neighbourhood(force, 'C02')
    >>> neighbourhood
    <Neighbourhood> C02

.. note:: You can use either a force ID or a Force object with
          ``get_neighbourhood()``.


Officers
^^^^^^^^

The contact details for each officer in a particular neighbourhood are
available::

    >>> neighbourhood.officers
    [<Neighbourhood.Officer> Michelle Zakoscielny, ..., <Neighbourhood.Officer> Richard Jones]


Events
^^^^^^

Neighbourhood-level events (beat meetings, surgeries, etc.) are available::

    >>> neighbourhood.events
    [<Neighbourhood.Event> Stocking Farm beat surgery, ..., <Neighbourhood.Event> Stocking Farm beat surgery]

Priorities
^^^^^^^^^^

Policing teams set priorities to deal with in their neighbourhoods, which are
represented by an *issue*, and an *action* to be taken::

    >>> neighbourhood.priorities
    [<Neighbourhood.Priority> <p>To address the issues of people begging next to cash machines in Market Street and surrounding area.</p>, ..., <Neighbourhood.Priority> <p>To reduce street drinking and associated anti-social behaviour on Conduit Street and London Road between 10am and 6pm each day.</p>]

Reference
---------

.. toctree::
    :maxdepth: 2

    forces
    neighbourhoods


.. _Police API: http://data.police.uk/docs/
.. _Police.uk: http://www.police.uk/
.. _README: https://github.com/rkhleics/police-api-client-python/
