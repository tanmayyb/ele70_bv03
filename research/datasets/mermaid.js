classDiagram
    %% Abstract IESODataset that both FSA and Zonal types extend
    class IESODataset {
        <<abstract>>
        +dataset_type: string
        +region: string
        +set_target(target_idx: int)
        +load_dataset(start_date, end_date, target_idx, download=True)
        +get_target_options()
        +parse_dataset(chunk_size=4)
        +save_dataset(filepath=None)
        +load_from_json(filepath=None)
    }

    %% IESO FSA variant
    class IESO_FSA {
        +dataset_type: string = "fsa"
        +region: string = "ON"
        +target_options: list
        +target_val: list
        +filetype: string = "zip"
        +date_type: string = "YYYYMM"
        +Data_Granularity: string = "FSA level consumption"
        +Data_Format: string = "Total consumption by postal code"
        +set_target(target_idx: int)
        +load_dataset(start_date, end_date, target_idx, download=True)
        +get_target_options()
        +parse_dataset(chunk_size=4)
        +save_dataset(filepath=None)
        +load_from_json(filepath=None)
    }
    IESO_FSA --|> IESODataset

    %% IESO Zonal variant
    class IESO_Zonal {
        +dataset_type: string = "zonal"
        +region: string = "ON"
        +target_options: list = ["Northwest", "Northeast", "Ottawa", "East", "Toronto", "Essa", "Bruce", "Southwest", "Niagara", "West", "Zone Total"]
        +target_val: string
        +filetype: string = "csv"
        +date_type: string = "YYYY"
        +Data_Granularity: string = "Zonal level demand"
        +Data_Format: string = "Demand by geographical zone"
        +set_target(target_idx: int)
        +load_dataset(start_date, end_date, target_idx, download=True)
        +get_target_options()
        +parse_dataset(chunk_size=4)
        +save_dataset(filepath=None)
        +load_from_json(filepath=None)
    }
    IESO_Zonal --|> IESODataset

    %% ClimateDataset that uses an IESODataset instance
    class ClimateDataset {
        +region: string = "ON"
        +dataset_type: string = "climate"
        +data_dir: string = "./data/climate"
        +default_filename: string = "climate_dataset.json"
        +dataset_name: string = "climate"
        +ieso_dataset: IESODataset
        +target_name: string
        +weather_station_ids: list
        +ieso_dataset_type: string
        +ieso_target_name: string
        +ieso_target_val: string
        +datetime_range: string
        +selected_station_ids: list
        +weather_stations: list
        +df: DataFrame
        +__init__(iesodata, region="ON")
        +load_dataset(sample_num=5, sampling_seed=42, download=True, filepath=None)
        +select_weather_stations()
        +perform_checks(df, start_dt, end_dt)
        +load_station_data(station_id)
        +combine_station_data()
        +get_weather_stations()
        +get_zone_based_weather_stations()
        +get_location_based_weather_stations()
        +save_dataset(filepath=None)
        +load_from_json(filepath=None)
    }
    ClimateDataset o-- IESODataset : uses

    %% Preprocessor that depends on both IESODataset and ClimateDataset
    class Preprocessor {
        +ieso_dataset: IESODataset
        +climate_dataset: ClimateDataset
        +target_name: string
        +init(ieso_dataset, climate_dataset)
        +preprocess(delete_leap_day=False)
        +save_dataset(filepath)
        +load_dataset(filepath) : tuple[string, DataFrame, datetime]
    }
    Preprocessor o-- IESODataset : uses
    Preprocessor o-- ClimateDataset : uses
