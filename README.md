# COVID-data-analysis
Collect and visualize various data sources related to COVID-19 for
research project at Columbia University.

## lockdown dates
Records the lockdown and reopen dates for different public services. Data is
obtained from [IHME covid](http://www.healthdata.org/covid/data-downloads)
and [IHME US geolocations](https://gist.github.com/Ryshackleton/42145c938f06d43cc3ddf75c3d7afd31).

For each location, the start/end date for restrictions on the following
event is contained:
- travel limit
- stay home
- educational facility
- any gathering
- any business
- all non-essential business

The [lockdown date](lockdown_dates/lockdown_date.csv) file contains the
information on worldwide locations; the [lockdown date US](lockdown_dates/lockdown_date_us.csv)
file contains the information for US states only.

## twitter geotag
Fetch the geolocation-related metadata with each tweet, including:
- `geo`: the geotag if user supplied one when sending the tweet
- `usr_location`: The location set by the user on user profile

A sample output can be found [here](twitter_geotag/sample_output.csv).

Note that a twitter developer account is needed to run the script. A Bearer token
needs to be supplied either in command line or in `twitter_geotag/twitter_authentication`
in form of:
```
API key: XXX
API key secret: XXX
Bearer token: XXX
```
Instructions on setting up twitter developer account and authentication
is [here](https://developer.twitter.com/en/docs/authentication/oauth-1-0a).
