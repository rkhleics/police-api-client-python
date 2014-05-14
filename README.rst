Police API Client (Python) |travis_badge|
=========================================

A Python client for the `Police API`_. Supports Python 2.6, 2.7, 3.2, 3.3 and
3.4.

Installation
------------

Install the Police API client with ``pip``::

    pip install police-api-client

Usage
-----

The Police API doesn't require authentication, so no setup is required::

    >>> from police_api import PoliceAPI
    >>> api = PoliceAPI()

Retrieving force & neighbourhood data::

    >>> api.get_forces()
    [<Force> Avon and Somerset Constabulary, ..., <Force> Wiltshire Police]
    >>> leicestershire = api.get_force('leicestershire')
    >>> city_centre = api.get_neighbourhood(leicestershire, 'city-centre-neighbourhood')
    >>> city_centre.description
    The Castle neighbourhood is a diverse covering all of the City Centre. In addition it covers De Montfort University, the Univesity of Leicester, Leicester Royal Infirmary, the Leicester Tigers rugby ground and the Clarendon Park and Riverside communities.
    ...
    >>> city_centre.contact_details
    {u'email': u'central.lpu@leicestershire.pnn.police.uk', u'telephone': u'101', u'address': u'74 Belgrave Gate\n, Leicester, LE1 3GG'}

Locating neighbourhoods::

    >>> n = api.locate_neighbourhood(52.63473, -1.137514)
    >>> n
    <Neighbourhood> C04
    >>> n.force
    <Force> Leicestershire Police

Crime & outcomes data::

    >>> api.get_latest_date()
    u'2013-09'
    >>> api.get_crimes_area(city_centre.boundary)
    [<Crime> 26926242, ..., <Crime> 26925710]
    >>> len(api.get_crimes_area(city_centre.boundary, date='2013-08'))
    810
    >>> crime = api.get_crimes_area(city_centre.boundary, date='2013-06')[0]
    >>> crime.outcomes
    [<Crime.Outcome> Under investigation, <Crime.Outcome> Suspect charged, <Crime.Outcome> Awaiting court outcome]

For more advanced usage, see the documentation_.

.. _Police API: http://data.police.uk/docs/
.. _documentation: http://police-api-client-python.readthedocs.org

.. |travis_badge| image:: https://api.travis-ci.org/rkhleics/police-api-client-python.svg
                       :target: https://travis-ci.org/rkhleics/police-api-client-python
