Installation
============

``pip install tally``


The tally Server
----------------

Tally can be easily added to your existing Django site:

1. Add ``tally`` to your ``INSTALLED_APPS``
2. Include ``tally.urls`` in your URLconf somewhere, for example::

    url(r'^_tally/', include('tally.urls'))

3. Run ``manage.py syncdb`` to create tally's Archive table
4. Create one or more Archives in the Django admin (or via the API, coming soon)
5. Run ``manage.py tallyserver`` to start listening for metrics

.. note:: Unless you want your metrics to be public, you should take care to protect the URLs using HTTP basic authentication, or some other method.
          You may also consider running a separate tally instance inside your network that your production site sends metrics to.


Sending Metrics
---------------

Use the ``tally.tally`` method to send a metric for aggregation:

.. autofunction:: tally.tally
