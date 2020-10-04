import cProfile, pstats, tracemalloc, pandas, statistics, copy, time
import data as dados
import configparser
import conf

from random import sample
from stream.redis import RedisStream
from classifiers import *

def print_memory(data):
    print(data[0])

def pre_execution(limit_data, redis_url, datasets=conf.DATASETS):
    dataset_path = conf.DATASETS_DISPONIVEIS['BASE_PATH']
    
    schema=training_data=actual_data=pca_components=data=columns=pca=denstream=cache=None

    files_scan = []
    files_benign = []
    texto = []
    for dataset in datasets:
        actual_dataset = conf.DATASETS_DISPONIVEIS[dataset]
        files_scan += [f'{dataset}\\{attack}' for attack in actual_dataset["attacks"]]
        files_benign.append(f'{dataset}\\{actual_dataset["benign"]}')
        texto.append(actual_dataset['descricao'])

    readed_data = []
    training_data = []
    #Ecobee tem o menor numero de amostras
    rows = int(13113/3)

    for file_benign in files_benign:
        data1, data2 = dados.get_data(dataset_path + file_benign, n=2*rows)
        data1 = data1.sample(n=limit_data)
        readed_data.append(data1)
        training_data2 = data2.values.tolist()
        training_data2 = [ list(map(str, data)) for data in training_data2 ]
        for row in training_data2:
            training_data.append(row)

    data = pandas.concat(readed_data)
    data = data.sample(n=limit_data)
    schema = data.columns.values.tolist()
    training_data = sample(training_data, 2*rows)
    data = [ list(map(str, d)) for d in data.values.tolist() ]
    training_data = data + training_data

    actual_data = {}
    for file in files_scan:
        name_file = file.split('\\')[-1].split('.')[0]
        scan_data, _ = dados.get_data(dataset_path + file, n=int(rows/8))
        scan_data = scan_data.values.tolist()
        actual_data[name_file] = [ list(map(str, data)) for data in scan_data ] 

    print(' | '. join(texto))

    cache = dados.send_cache(schema, training_data, actual_data, redis_url)
    return cache

def execution(cache, number_devices, minPts, pca_components, limit_data):
    try:
        # cache = RedisStream(None, None, None, host='192.168.0.75', mounting=False)
        # number_devices = 9
        minPts = 3
        pca_components = 1
        schema_path = conf.DATASETS_DISPONIVEIS['BASE_PATH'] + conf.DATASETS_DISPONIVEIS['BASE_SCHEMA']

        schema = pandas.read_csv(schema_path).columns.tolist()
        data_array = []

        number_data = number_devices*limit_data

        while len(data_array) <= (number_data):
            data = cache.get_training_stream()
            array = data.decode('utf-8').split(';')
            data_array.append(list(map(float, array)))

        data = pandas.DataFrame(data_array, columns=schema)
        actual_data = None

        classifier = DenStreamModel(schema, minPts, pca_components)
        data = classifier.preprocessing_training_data(data, actual_data)
        
        classifier.offline(data, number_data, number_devices)
        
        classifier.run_async(cache)
    except Exception as exc:
        print(exc)
    finally:
        cache.clean()
        print('Clean cache')


if __name__ == '__main__':

    config = configparser.ConfigParser()
    config.read('conf.ini')

    DATASETS = config['DATASETS']['DATASETS'].split(',')
    redis_url = config['DEFAULT']['REDIS_URL']
    limit_data = int(config['DEFAULT']['NUMBER_SAMPLES'])
    runs = int(config['DEFAULT']['NUMBER_RUNS']) + 1
    pca_components = int(config['DEFAULT']['PCA_COMPONENTS'])
    minPts = int(config['DEFAULT']['MIN_PTS'])

    # pre_execution()
    

    for i in range(1,runs):
        print(f'Execution # {i} \n')
        cache = pre_execution(limit_data, redis_url, DATASETS)
        execution(cache, len(DATASETS), minPts, pca_components, limit_data)
        