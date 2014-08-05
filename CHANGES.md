0.4.0
=====

    - Updated `tally.tally` to allow sending multiple metrics at once
    - Added a `tally.archives` convenience method to return a QuerySet of Archives
    - Changed `Archive.aggregate` to order values by the aggregate field first, if specified


0.3.0
=====

    - Renamed `listen` management command to `tallyserver` to avoid potential conflicts with other apps
    - Updated `tally.tally` to record metrics locally if no `host` is specified, and `TALLY_HOST` is `None`
