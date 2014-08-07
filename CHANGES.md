0.5.0
=====

- Started a test suite
- Changed `Archive.timedata` to return data in order from earliest to latest, and added a `reverse` flag
- Simplified setup.py, switched to setuptools


0.4.1
=====

- Added an `Archive.timedata` method to return aggregated data for all possible timepoints, not just those with data
- Started using Django 1.7 migrations


0.4.0
=====

- Updated `tally.tally` to allow sending multiple metrics at once
- Added a `tally.archives` convenience method to return a QuerySet of Archives
- Changed `Archive.aggregate` to order values by the aggregate field first, if specified


0.3.0
=====

- Renamed `listen` management command to `tallyserver` to avoid potential conflicts with other apps
- Updated `tally.tally` to record metrics locally if no `host` is specified, and `TALLY_HOST` is `None`
