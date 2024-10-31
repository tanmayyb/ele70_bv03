#######
# Paste code below into your script to access our API/functions
#######
# import urllib.request
# api_url = 'https://raw.githubusercontent.com/tanmayyb/tmu-capstone-anomaly-detection/refs/heads/main/api/imports/apis.py'
# exec(urllib.request.urlopen(api_url).read())

import pandas as pd

# Dataloader for Energy Demand (IESO Zonal Ontario-wide)
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

      # add datetime
      df['DateTime'] = pd.to_datetime(df['Date'], utc=False)+pd.to_timedelta(df['Hour'], unit='h')

      if not join:
        dataset[year] = df
      else:
        dataset = pd.concat([dataset, df])

    return dataset

# Dataloader for Weather (Canada-Wide)
def load_climate_dataset(first_year:int, last_year:int, station_id:int=31688, join:bool=False) -> dict|pd.DataFrame:

  # assertion checks
  assert first_year <= last_year, "invalid entry for first/last year"
  assert first_year>=2003, "invalid entry for first_year, please select >=2003"
  assert last_year<=2024, "invalid entry for last year"

  # hourly data for a given year, and station
  # f'https://climate.weather.gc.ca/climate_data/bulk_data_e.html?format=csv&time=UTC&stationID=31688&Year=2008&Month={i}&timeframe=1&submit=Download+Data'

  num_years = last_year - first_year

  url_prefix = 'https://climate.weather.gc.ca/climate_data/bulk_data_e.html?format=csv'
  timeframe = 1

  if num_years<=0:
    tmp = []
    for month in range(1, 12+1):
      url = url_prefix+f'&time=UTC&stationID={station_id}&Year={first_year}&Month={month}&timeframe={timeframe}&submit=Data'
      tmp.append(pd.read_csv(url))
    df = pd.concat(tmp)
    return df

  else:
    # data = dict()
    if not join:
      data = dict()
    else:
      data = pd.DataFrame()

    for year in tqdm(range(first_year, last_year+1)):
      tmp = []
      for month in range(1, 12+1):
        url = url_prefix+f'&time=UTC&stationID={station_id}&Year={year}&Month={month}&timeframe={timeframe}&submit=Data'
        tmp.append(pd.read_csv(url))
      tmp = pd.concat(tmp)
      
      if not join:
        data[year] = tmp
      else:
        data = pd.concat([data, tmp])
    return data