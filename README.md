## ELE70A/B Capstone - Forecast Energy Demand with Weather!
 

## Requirements
1. Conda:
   1. Install Conda ([exe](https://repo.anaconda.com/archive/Anaconda3-2024.10-1-Windows-x86_64.exe)) (select all options)

2. Git:
   1. Download Git for Windows from (https://git-scm.com/download/win)
   2. Run the downloaded installer (Git-X.XX.X-64-bit.exe)
   3. Accept the default settings during installation
   4. Open Command Prompt and verify Git is installed by running:
      ```
      git --version
      ```

## Setup
With terminal (command prompt/powershell) open at a directory of your choice, run the following commands:
1. clone the repository:
    ```
    git clone https://github.com/tanmayyb/ele70_bv03.git
    ```
2. navigate to the repository:
    ```
    cd ele70_bv03
    ```
 3. Run `setup.bat`:
    ```
    setup.bat
    ```
 4. Run `env.bat`:
    ```
    call env.bat
    ```
    Use this to activate the virtual environment each time you open a new terminal. Use `deactivate` to exit the virtual environment.
 5. Run `pip install -r requirements.txt`:
    ```
    pip install -r requirements.txt
    ```


## Dataset Formatter

```
> python parse.py -h

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

> python parser.py --input_filepath "INPUT_FILE_Load_Forecasgin.xlsx" --output_filepath "my_cute_dataset.csv"
```

