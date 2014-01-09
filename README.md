tally
=====

A Django application (and daemon) for collecting, storing, and aggregating metrics.

Installation
============

1. ```pip install tally```
2. Add ```tally``` to your ```INSTALLED_APPS``` setting.
3. Set ```TALLY_DATA_DIR``` to a directory where tally's metrics should be stored.
4. (Optional) Include ```tally.urls``` in your URLconf. This will provide access to the dashboard and JSON API for retrieving metric data.
5. ```manage.py syncdb```
6. ```manage.py listen```

Basic Usage
===========

You can send metrics from anywhere in your code using the following:

```python
import tally
tally.tally(metric_name) # Assumes a value of 1 (i.e. a counter)
tally.tally(metric_name, value) # Assumes the current timestamp
tally.tally(metric_name, value, timestamp)
```

```tally.tally``` also accepts ```host``` and ```port``` keyword arguments, in case the listener is on another server.

Request Timing
==============

Tally includes a simple page timing middleware, ```tally.middleware.PageTimingMiddleware```. Requests are logged in the format:

    requests.[method].[part-part].[path-part]

For example, a GET request for ```/hello/world/``` would be logged as ```requests.get.hello.world```.
