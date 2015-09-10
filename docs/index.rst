Police API Client (Python)
==========================

.. currentmodule:: police_api
.. py:module:: police_api

The Police API Client is an open-source client for the `Police API`_. It was
built to power the new Police.uk_ website.

View the README_ for installation instructions and quick-start examples.

Reference
---------

.. toctree::
   :maxdepth: 2
   :glob:

   reference/police_api
   reference/forces
   reference/neighbourhoods
   reference/crime

Configuration
-------------

The API doesn't require any configuration or authentication, so all you need to
do to get going is make a PoliceAPI instance::

    >>> from police_api import PoliceAPI
    >>> api = PoliceAPI()

Fore available methods and configuration parameters, see the :class:`PoliceAPI`
reference.


Forces
------

To retrieve a list of police forces, use :func:`PoliceAPI.get_forces`::

    >>> api.get_forces()
    [<Force> Avon and Somerset Constabulary, ..., <Force> Wiltshire Police]

If you know the ID of a particular force, then you can use :func:`PoliceAPI.get_force`::

    >>> force = api.get_force('leicestershire')
    >>> force
    <Force> Leicestershire Police

Fore available attributes and methods, see the :class:`forces.Force` reference.


Neighbourhoods
--------------

Forces are broken down into *Neighbourhood Policing Teams*::

    >>> force.neighbourhoods
    [<Neighbourhood> C02, <Neighbourhood> L03, ..., <Neighbourhood> L69]

If you know the ID of a particular neighbourhood, then you can use
:func:`PoliceAPI.get_neighbourhood`::

    >>> neighbourhood = api.get_neighbourhood('leicestershire', 'C02')
    >>> neighbourhood
    <Neighbourhood> C02

Or, if you already have a Force object::

    >>> neighbourhood = force.get_neighbourhood('C02')
    >>> neighbourhood
    <Neighbourhood> C02

Fore available attributes and methods, see the
:class:`neighbourhoods.Neighbourhood` reference.


Officers
^^^^^^^^

The contact details for each officer in a particular neighbourhood are
available::

    >>> neighbourhood.officers
    [<Neighbourhood.Officer> Michelle Zakoscielny, ..., <Neighbourhood.Officer> Richard Jones]

Fore available attributes and methods, see the
:class:`neighbourhoods.Neighbourhood.Officer` reference.


Events
^^^^^^

Neighbourhood-level events (beat meetings, surgeries, etc.) are available::

    >>> neighbourhood.events
    [<Neighbourhood.Event> Stocking Farm beat surgery, ..., <Neighbourhood.Event> Stocking Farm beat surgery]

Fore available attributes and methods, see the
:class:`neighbourhoods.Neighbourhood.Event` reference.


Priorities
^^^^^^^^^^

Policing teams set priorities to deal with in their neighbourhoods, which are
represented by an *issue*, and an *action* to be taken::

    >>> neighbourhood.priorities
    [<Neighbourhood.Priority> <p>To address the issues of people begging next to cash machines in Market Street and surrounding area.</p>, ..., <Neighbourhood.Priority> <p>To reduce street drinking and associated anti-social behaviour on Conduit Street and London Road between 10am and 6pm each day.</p>]

Fore available attributes and methods, see the
:class:`neighbourhoods.Neighbourhood.Priority` reference.


Crime & Outcomes
----------------

The crime data is updated monthly, and each data set is represented by a date
string, in the format ``YYYY-MM``::

    >>> api.get_dates()
    [u'2014-03', u'2014-02', u'2014-01', ..., u'2010-12']
    >>> api.get_latest_date()
    u'2014-03'

To get crimes within a particular neighbourhood, call
:func:`PoliceAPI.get_crimes_area` with that neighbourhood's boundary::

    >>> pprint(api.get_crimes_area(neighbourhood.boundary))
    [<Crime> 30412621,
     <Crime> 30412622,
     <Crime> 30409577,
     <Crime> 30411516,
     ...
     <Crime> 30410475,
     <Crime> 30412775,
     <Crime> 30411518,
     <Crime> 30412182]

To fetch data for months other than the latest one, use a date string like the
ones returned by :func:`PoliceAPI.get_dates`::

    >>> pprint(api.get_crimes_area(neighbourhood.boundary, date='2013-10'))
    [<Crime> 27566767,
     <Crime> 27573059,
     <Crime> 27570299,
     <Crime> 27570923,
     ...
     <Crime> 27569847,
     <Crime> 27570896,
     <Crime> 27571396,
     <Crime> 27570916]

Crimes contain the date, category and location::

    >>> crime = api.get_crime('ddf4c172d29569ab0cb667a346bcffad18f54a9bc3e0ae9694d2daf6738f068b')
    >>> crime
    <Crime> 20325597
    >>> crime.month
    u'2013-01'
    >>> crime.category
    <CrimeCategory> Shoplifting
    >>> crime.location
    <Location> 701166
    >>> crime.location.name, crime.location.latitude, crime.location.longitude
    (u'On or near Constance Close', u'51.737837', u'-2.235178')

Crimes have a list of outcomes, which represents the timeline of events since
the crime was reported::

    >>> pprint(crime.outcomes)
    [<Crime.Outcome> Under investigation,
     <Crime.Outcome> Suspect charged,
     <Crime.Outcome> Awaiting court outcome,
     <Crime.Outcome> Offender imprisoned]
    >>> crime.outcomes[-1].date
    u'2013-01'

Crime objects representing Anti-Social Behaviour will not have outcomes::

   >>> asb = api.get_crimes_area(neighbourhood.boundary, category='anti-social-behaviour')[0]
   >>> asb.outcomes
   []

For available attributes and methods, see the :class:`crime.Crime` reference.


.. _Police API: https://data.police.uk/docs/
.. _Police.uk: https://www.police.uk/
.. _README: https://github.com/rkhleics/police-api-client-python/
