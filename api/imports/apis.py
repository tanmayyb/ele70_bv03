#######
# Paste code below into your script to access our API/functions
#######
# import urllib.request
# api_url = 'https://raw.githubusercontent.com/tanmayyb/tmu-capstone-anomaly-detection/refs/heads/main/api/imports/apis.py'
# exec(urllib.request.urlopen(api_url).read())

import pandas as pd

# Dataloader
def load_ieso_dataset( first_year:int, last_year:int, join:bool=False) -> dict|pd.DataFrame:
  # loads dataset from multiple years

  # assertion checks
  assert first_year <= last_year, "invalid entry for first/last year"
  assert first_year>=2003, "invalid entry for first_year, data before 2003 is N/A"
  assert last_year<=2024, "invalid entry for last year"

  # prefix and suffix defined for IESO api
  url_prefix = 'http://reports.ieso.ca/public/DemandZonal/PUB_DemandZonal_'
  url_suffix = '.csv'

  if first_year == last_year:
    # only for 1 year
    url = url_prefix+str(first_year)+url_suffix
    return pd.read_csv(url, header=3) # returns record
  else:
    # multiple years
    # decide dataset data type based on
    # if user wants a joined dataset
    if not join:
      dataset = dict()
    else:
      dataset = pd.DataFrame()

    # multiple year data
    for year in range(first_year, last_year+1):
      url = url_prefix+str(year)+url_suffix
      df = pd.read_csv(url, header=3) # returns record

      if not join:
        dataset[year] = df
      else:
        dataset = pd.concat([dataset, df])

    return dataset

