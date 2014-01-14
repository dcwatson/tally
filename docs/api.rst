Tally API
=========

The real power of tally lies in its JSON API. Each API endpoint accepts the following GET parameters:

* ``q``: a glob pattern (e.g. ``requests.get.*``) for matching metric names
* ``since``: earliest timestamp to return metrics for
* ``until``: latest timestamp to return metrics for
* ``pretty``: indicates the JSON should be pretty-printed (useful for debugging or just playing around)


Values
------

These API endpoints return metrics broken down by both metric name and timestamp.

``/values/<slug>/``
    Returns a dictionary of metric keys contained in the archived identified by ``<slug>``, each mapping to a dictionary of timestamps with all aggregate values.

``/values/<slug>/by<time|name>/``
    Breaks down the values by time or name. Note that this indicates the "second-level" breakdown, so specifying "byname"
    will first break down values by time, then by name.

``/values/<slug>/<aggregate>/``
    Returns the same breakdown as ``/values/<slug>/``, but only returns the specified aggregate, instead of all aggregates.
    ``<aggregate>`` may be one of: ``avg``, ``min``, ``max``, ``sum``, or ``count``.

``/values/<slug>/<aggregate>/by<time|name>/``
    Returns the specified aggreagte, broken down by either time or name.


Aggregates
----------

These API endpoints return metrics broken down only by name or timestamp, then aggregated. So if broken down by name (for instance), instead of returning metrics
for every timestamp, the metrics are appropriately aggregated (summing ``count`` and ``sum``, averaging ``avg``, etc.) and one value is returned per name.

``/aggregate/<slug>/``
    Returns aggregated metrics for each timestamp. Equivalent to ``/aggregate/<slug>/bytime/``.

``/aggregate/<slug>/by<time|name>/``
    Returns aggregated metrics for names or timestamps.

``/aggregate/<slug>/<aggregate>/``
    Returns only the specifed aggregate per timestamp.

``/aggregate/<slug>/<aggregate>/by<time|name>/``
    Returns only the specified aggregate per name or timestamp.


Useful Examples
---------------

Imagine an archive named "daily" that records page request timings with a 10 second resolution and 24 hour retention, via the ``PageTimingMiddleware`` (see :ref:`middleware`):

``/aggregate/daily/avg/``
    This will return all timestamps for the last 24 hours (every 10 seconds), along with the average request time for each 10 second window.
