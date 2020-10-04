# Detecting IoT Botnet Formation Using Data Stream Clustering Algorithms (DenStream)

Code for experimentation used on the paper published on Webist 2020 - DMMLACS . In this experiments was used _DenStream_.

## Dataset

[N-BaIoT: Network-based Detection of IoT Botnet Attacks Using Deep Autoencoders](https://archive.ics.uci.edu/ml/datasets/detection_of_IoT_botnet_attacks_N_BaIoT).

## Usage

The version of Python used was 3.6.5

Install dependencies:
```
pip install -r requirements.txt
```

Execute Redis server:
```
redis-server
```

Execution:
```
python main.py
```

conf.py
```
BASE_PATH': '<<Base path of dataset on the machine>>',
    'BASE_SCHEMA': 'demonstrate_structure.csv',
    '<<folder name within BASE_PATH of the device>>': {
        'descricao': '<<description>>', 
        'benign': '<< name of benign file within the folder. usually benign_traffic.csv>>',
        'attacks': [
            <<list of file names within the folder which contains the attacks to be used of this device>>
        ]
    },
    ...
```

conf.ini
```
[DEFAULT]
NUMBER_SAMPLES=Number of samples to be used on training
NUMBER_RUNS=Number of executions in a rown wanted
PCA_COMPONENTS=Number of Components to be used after PCA
MIN_PTS=Number of minpts used on denstream
REDIS_URL=localhost

[DATASETS]
ALL_DATASETS=List of all folder names available on conf.py, separated by comma
DATASETS=List of all folder names wanted on experimentation, separated by comma
```