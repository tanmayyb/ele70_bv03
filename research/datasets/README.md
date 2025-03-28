# DataLoaders


1. [IESO](#ieso)
2. [Climate](#climate)
3. [Preprocessor](#preprocessor)
4. [Dataset API Usage/Workflow](#dataset-api-usageworkflow)


## API Reference

### IESO
| Property | FSA Type | Zonal Type |
|----------|----------|------------|
| dataset_type | "fsa" | "zonal" |
| region | Only "ON" supported | Only "ON" supported |
| target_options | List of Ontario cities | Fixed list: ["Northwest", "Northeast", "Ottawa", "East", "Toronto", "Essa", "Bruce", "Southwest", "Niagara", "West", "Zone Total"] |
| target_val | List of postal codes for selected city | Same as selected zone name |
| filetype | "zip" | "csv" |
| date_type | Monthly (YYYYMM) | Yearly (YYYY) |
| Data Granularity | FSA (Forward Sortation Area) level consumption | Zonal level demand |
| Data Format | Total consumption by postal code | Demand by geographical zone |


| Method | FSA Type | Zonal Type |
|--------|----------|------------|
| set_target(target_idx: int) | Sets city and corresponding postal codes<br>Example: set_target(0) might select "Toronto" and its FSAs | Sets single zone name<br>Example: set_target(4) selects "Toronto" zone |
| load_dataset(start_date, end_date, target_idx, download=True) | start_date: YYYYMM format (e.g., 201801)<br>end_date: YYYYMM format<br>Example: load_dataset(201801, 201812, 0, download=True) | start_date: YYYY format (e.g., 2018)<br>end_date: YYYY format<br>Example: load_dataset(2018, 2018, 4, download=True) |
| get_target_options() | Returns list of available cities | Returns list of 11 zones:<br>["Northwest", "Northeast", "Ottawa", etc.] |
| parse_dataset(chunk_size=4) | Processes FSA consumption data<br>Groups by DATE, HOUR for selected postal codes | Processes zonal demand data<br>Direct selection of zone column |
| save_dataset(filepath=None) | Saves data with FSA metadata:<br>- City name<br>- Postal codes<br>- Monthly files | Saves data with zonal metadata:<br>- Zone name<br>- Yearly files |
| load_from_json(filepath=None) | Loads FSA dataset with:<br>- Consumption by postal code<br>- DateTime in monthly granularity | Loads zonal dataset with:<br>- Demand by zone<br>- DateTime in yearly granularity |
### Climate
| Property/Attribute | Description |
|-------------------|-------------|
| region | Region for which climate data is collected (default: "ON") |
| dataset_type | Fixed as "climate" |
| data_dir | Directory for storing climate data (default: "./data/climate") |
| default_filename | Default filename for saving dataset (default: "climate_dataset.json") |
| dataset_name | Fixed as "climate" |
| ieso_dataset | Reference to an IESODataset instance that provides location information |
| target_name | Target name inherited from the IESO dataset |
| weather_station_ids | IDs of weather stations |
| ieso_dataset_type | Type of the IESO dataset ("fsa" or "zonal") |
| ieso_target_name | Target name from the IESO dataset |
| ieso_target_val | Target value from the IESO dataset |
| datetime_range | Date range inherited from the IESO dataset |
| selected_station_ids | List of selected weather station IDs |
| weather_stations | Collection of selected weather stations based on IESO data locations |
| df | The loaded climate dataset containing weather measurements |

| Method | Description |
|--------|-------------|
| __init__(iesodata, region="ON") | Initializes the ClimateDataset with an IESODataset reference |
| load_dataset(sample_num=5, sampling_seed=42, download=True, filepath=None) | Loads climate data with specified sampling parameters, will load local dataset if download=False |
| select_weather_stations() | Selects appropriate weather stations based on IESO data locations |
| perform_checks(df, start_dt, end_dt) | Validates the dataset for completeness within the specified date range |
| load_station_data(station_id) | Loads weather data for a specific station ID |
| combine_station_data() | Combines data from multiple weather stations with appropriate column prefixes |
| get_weather_stations() | Determines which method to use for selecting weather stations based on IESO dataset type |
| get_zone_based_weather_stations() | Selects weather stations based on geographical zones (used for zonal IESO data) |
| get_location_based_weather_stations() | Selects weather stations based on specific locations (used for FSA IESO data) |
| save_dataset(filepath=None) | Saves the dataset to a JSON file at the specified filepath or a default location |
| load_from_json(filepath=None) | Loads a previously saved dataset from a JSON file |

### Preprocessor

| Property/Attribute | Description |
|-------------------|-------------|
| ieso_dataset | Reference to an IESODataset instance containing energy demand data |
| climate_dataset | Reference to a ClimateDataset instance containing weather data |
| target_name | Target name inherited from the IESO dataset (e.g., zone name or city) |

| Method | Description |
|--------|-------------|
| __init__(ieso_dataset, climate_dataset) | Initializes the Preprocessor with IESO and Climate datasets |
| preprocess(delete_leap_day=False) | Merges IESO and climate data, adds time features (Y,M,D,H), performs basic cleaning, and returns the target name and processed dataframe |

## Usage

0. The app loads the API through github
```Python
import urllib.request
api_url = 'https://raw.githubusercontent.com/tanmayyb/ele70_bv03/refs/heads/main/api/datasets.py'
exec(urllib.request.urlopen(api_url).read())
```

### IESO Dataset

1. User chooses which IESO dataset they would like to load (`zonal` or `fsa`), and the app creates the relevant object
```Python
ieso = IESODataset('fsa')
or 
ieso = IESODataset('zonal')
```

2. The API can then be used by the app to give user options for target and datetime range

```Python
target_options = ieso.get_target_options() # returns list of the target options
available_dates = ieso.get_dates() # returns list of available dates (str)
```
Note: the variables above can be used to show user options for target and datetime range

3. App can load the ieso dataset using a load_dataset call
```Python
ieso.load_dataset(start_date=<str>, end_date=<str>, download=True)
```

### Climate Dataset
1. Climate Dataset can be easily created by the app by just passing the ieso dataset
```Python
climate = ClimateDataset(ieso)
```

2. The climate dataset can be loaded using a load_dataset call
```Python
climate.load_dataset(sample_num=5, download=True)
```
Note: The user can also select how many weather stations they would like to sample

### Preprocessor

1. To get the processed dataset for machine learning, the app needs to pass the ieso and climate dataset objects into a preprocessor 
```Python
preprocessor = DatasetPreprocessor(ieso, climate)
target_name, dataset = preprocessor.preprocess()
```

That;s it!


## Algorithms

### Weather Station Sampling Algorithm 

<div style="display: flex;">
  <img src="img/climate_zonal_nw.png" alt="Climate Zonal NW" width="50%" height="50%">
  <img src="img/climate_zonal_sw.png" alt="Climate Zonal SW" width="50%" height="50%">
</div>

- Fast filtering for weather station based on zonal bounding box
- More precise filtering done by selecting filtered points within geometric boundary of zones