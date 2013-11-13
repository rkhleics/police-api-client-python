police-api-client-python
========================

This is an unofficial Python client for the `Police API`_.

Installation
------------

Install the Police API client with ``pip``::

    pip install police_api

Usage
-----

The Police API doesn't require authentication, so no setup is required.

Retrieving information about police forces and neighbourhoods is simple::

    >>> from police_api import PoliceAPI
    >>> api = PoliceAPI()
    >>> api.get_forces()
    [<Force> Avon and Somerset Constabulary, ..., <Force> Wiltshire Police]
    >>> leicestershire = api.get_force('leicestershire')
    >>> city_centre = api.get_neighbourhood(leicestershire, 'city-centre-neighbourhood')
    >>> city_centre.description
    The Castle neighbourhood is a diverse covering all of the City Centre. In addition it covers De Montfort University, the Univesity of Leicester, Leicester Royal Infirmary, the Leicester Tigers rugby ground and the Clarendon Park and Riverside communities.
    ...
    >>> city_centre.contact_details
    {u'email': u'central.lpu@leicestershire.pnn.police.uk', u'telephone': u'101', u'address': u'74 Belgrave Gate\n, Leicester, LE1 3GG'}

Getting crimes is easy, too::

    >>> api.get_latest_date()
    2013-09
    >>> api.get_crimes_area(city_centre.boundary)
    [<Crime> 26926242, ..., <Crime> 26925710]
    >>> len(api.get_crimes_area(city_centre.boundary, date='2013-08'))
    810

.. _Police API: http://data.police.uk/docs/
