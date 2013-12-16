Police API Client (Python)
==========================

The Police API Client is an unofficial open-source client for the `Police
API`_. It was built to power the new Police.uk_ website.

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
    >>> api = PoliceAPI(username='weroc42', password='abc123')
    >>> api.get_dates()
    [u'2013-10', u'2013-09', u'2013-08', ..., u'2010-12']
    >>> api.get_latest_date()
    u'2013-10'

This can then be used to filter the crimes by date::

    >>> api.get_crimes_point(52.63473, -1.137514, date='2013-08')

.. _Police API: http://data.police.uk/docs/
.. _Police.uk: http://www.police.uk/
.. _README: https://github.com/rkhleics/police-api-client-python/
