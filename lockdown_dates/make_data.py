"""
This script pulls the most updated information on public service/event lockdown date
from IHME website.
"""

import os
import pandas as pd

ihme_url = 'https://ihmecovid19storage.blob.core.windows.net/latest/ihme-covid19.zip'
zip_fname = 'ihme-covid19.zip'
data_fname = 'Summary_stats_all_locs.csv'
geo_fname = "ihme-us-location-ids.csv"

# download and process IHME data
if os.path.isfile(zip_fname):
    os.system('rm -f {}'.format(zip_fname))
os.system('wget {}'.format(ihme_url))
if not os.path.isfile(zip_fname):
    print("Error downloading data from {}".format(ihme_url))
    exit(0)
os.system('unzip {}'.format(zip_fname))
dir_name = None
for dname in os.listdir():
    if os.path.isdir(dname):
        if os.path.isfile(os.path.join(dname, data_fname)):
            dir_name = dname
os.system('cp {} {}'.format(os.path.join(dir_name, data_fname), data_fname))
os.system('rm -rf {}'.format(dir_name))
os.system('rm -rf {}'.format(zip_fname))

# processing Summary_stats_all_locs.csv
os.system('rm -rf {}'.format('lockdown_date.csv'))
os.system('rm -rf {}'.format('lockdown_date_us.csv'))

event_names = ["travel_limit",
               "stay_home",
               "educational_fac",
               "any_gathering_restrict",
               "any_business",
               "all_non-ess_business"]

raw_df = pd.read_csv(data_fname)
selected_columns = ['location_name', 'location_id']
for event in event_names:
    selected_columns.append(event + '_start_date')
    selected_columns.append(event + '_end_date')
for cname in selected_columns:
    assert(cname in set(raw_df.columns))

df = raw_df[selected_columns]

geo_df = pd.read_csv(geo_fname)[['location_id', 'FIPS']]
us_df = pd.merge(geo_df, df, on='location_id')

df.to_csv('lockdown_date.csv')
us_df.to_csv('lockdown_date_us.csv')
os.system('rm -f {}'.format(data_fname))
