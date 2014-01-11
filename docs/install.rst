Installation
============

``pip install tally``


Using tally as an application
-----------------------------

Tally can be easily added to your existing Django site:

1. Add ``tally`` to your ``INSTALLED_APPS``
2. Include ``tally.urls`` in your URLconf somewhere, for example::

    url(r'^_tally/', include('tally.urls'))

3. Run ``manage.py syncdb`` to create tally's Archive table
4. Run ``manage.py listen`` to start listening for metrics

.. note:: Unless you want your metrics to be public, you should take care to protect the URLs using HTTP basic authentication, or some other method.


Using tally as a standalone service
-----------------------------------

If you want to use tally's dashbaord or API, but do not want to include the URLs in your production site, you may want to run a separate standalone tally site.


Sending Metrics
---------------

Use the ``tally.tally`` method to send a metric for aggregation:

.. autofunction:: tally.tally
