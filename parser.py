# script to parse the data from xlsx file to csv file
# the xlsx file is the output of the data from the data source
# the csv file is the input for the models

import pandas as pd
import argparse

class PreserveFormattingHelpFormatter(argparse.RawDescriptionHelpFormatter):
    def _format_text(self, text):
        return text

def parse_data(args):
    input_filepath = args.input_filepath
    output_filepath = args.output_filepath
    target_name = args.target_name
    dataset_type = args.dataset_type

    # read the xlsx file
    print(f"Reading file: {input_filepath}")
    df = pd.read_excel(input_filepath)

    print(f"Writing file: {output_filepath}")
    metadata = {
    'target_name': target_name,
    'dataset_type': dataset_type,
    'column_types': {col: str(dtype) for col, dtype in df.dtypes.items()}
    }
    with open(output_filepath, 'w') as f:
        for key, value in metadata.items():
            f.write(f"# {key}: {value}\n")
        df.to_csv(f, index=False)

    print(f"File written: {output_filepath}")

if __name__ == "__main__":
    import datetime
    
    splash_art = \
"""                                                                                                       
     ┌────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────┐       
     │                                                                                                                        │       
     │          .sS$$$$$$$$$$$$$$Ss.                          `7MM"'"Yp, `7MMF'   `7MF'                                       │       
     │         .$$$$$$$$$$$$$$$$$$$$$$s.                        MM    Yb   `MA     ,V                                         │       
     │         $$$$$$$$$$$$$$$$$$$$$$$$S.                       MM    dP    VM:   ,V ,pP""Yq.   pd""b.                        │       
     │         $$$$$$$$$$$$$$$$$$$$$$$$$$s.                     MM"'"bg.     MM.  M'6W'    `Wb (O)  `8b                       │       
     │         S$$$$'        `$$$$$$$$$$$$$                     MM    `Y     `MM A' 8M      M8      ,89                       │       
     │         `$$'            `$$$$$$$$$$$.                    MM    ,9      :MM;  YA.    ,A9    ""Yb.                       │       
     │          :               `$$$$$$$$$$$                  .JMMmmmd9        VF    `Ybmmd9'        88                       │       
     │         :                 `$$$$$$$$$$                                                   (O)  .M'                       │       
     │      .====.  ,=====.       $$$$$$$$$$                                                    bmmmd'                        │       
     │    .'      ~'       ".    s$$$$$$$$$$                                                                                  │       
     │    :       :         :=_  $$$$$$$$$$$                                                                                  │       
     │    `.  ()  :   ()    ' ~=$$$$$$$$$$$'                                                                                  │       
     │      ~====~`.      .'    $$$$$$$$$$$                                                                                   │       
     │       .'     ~====~     sS$$$$$$$$$'                                                                                   │       
     │       :      .         $$$$$' $$$$                                                                                     │       
     │     .sS$$$$$$$$Ss.     `$$'   $$$'                                                                                     │       
     │    $$$$$$$$$$$$$$$s         s$$$$    `7MM"'"YMM                                           mm     mm                    │       
     │    $SSSSSSSSSSSSSSS$        $$$$$      MM    `7                                           MM     MM                    │       
     │         :                   $$$$'      MM   d  ,pW"Wq.`7Mb,od8 `7MMpMMMb.pMMMb.   ,6"Yb.mmMMmm mmMMmm .gP"Ya `7Mb,od8  │       
     │          `.                 $$$'       MM""MM 6W'   `Wb MM' "'   MM    MM    MM  8)   MM  MM     MM  ,M'   Yb  MM' "'  │       
     │            `.               :          MM   Y 8M     M8 MM       MM    MM    MM   ,pm9MM  MM     MM  8M""""""  MM      │       
     │             :               :          MM     YA.   ,A9 MM       MM    MM    MM  8M   MM  MM     MM  YM.    ,  MM      │       
     │             :              .'`.      .JMML.    `Ybmd9'.JMML.   .JMML  JMML  JMML.`Moo9^Yo.`Mbmo  `Mbmo`Mbmmd'.JMML.    │       
     │            .'.           .'   :                                                                                        │       
     │           : .$s.       .'    .'                                                                                        │       
     │           :.S$$$S.   .'    .'                                                                                          │       
     │           : $$$$$$`.'    .'                                                                                            │       
     │              $$$$   `. .'                                                                                              │       
     │                       `                                                                                                │       
     │                                                                                                                        │       
     │                                                                                                                        │       
     └────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────┘       
"""
    
    parser = argparse.ArgumentParser(
        description=splash_art,
        formatter_class=PreserveFormattingHelpFormatter
    )
    parser.add_argument('--input_filepath', type=str, required=True, help='Path to the xlsx file')
    parser.add_argument('--output_filepath', type=str, help='Path to the output csv file', default=f"data_{datetime.datetime.now().strftime('%Y%m%d_%H%M%S')}.csv")
    parser.add_argument('--target_name', type=str, help='Target name', default="Load Power (kW)")
    parser.add_argument('--dataset_type', type=str, help='Dataset type', default="user_input")
    args = parser.parse_args()
    parse_data(args)


    




