import time
import pandas

from stream.redis import RedisStream

def get_data(path, n=None, frac=None):
    data_initial = pandas.read_csv(path)
    if n:
        data_selected = data_initial.sample(n=n)
        data_excluded = data_initial[~data_initial.isin(data_selected)].dropna()
    elif frac:
        data_selected = data_initial.sample(frac=frac)
        data_excluded = data_initial[~data_initial.isin(data_selected)].dropna()
    else:
        data_selected = data_initial
        data_excluded = None
    return data_selected, data_excluded

def read_data(dataset_path, files, frac=(2/3), balanced=False):
    start = time.time()

    actual_data = {}

    data, training_data = get_data(dataset_path + files[0], frac=frac)
    schema = training_data.columns.values.tolist()
    rows_test = len(training_data.index)
    training_data = training_data.values.tolist()
    training_data = [ list(map(str, data)) for data in training_data ] 

    if balanced:
        rows_test = int(rows_test / (len(files) - 1) )

    for file in files[1:]:
        name_file = file.split('\\')[-1].split('.')[0]
        print('Lendo dados do ataques', name_file)
        read_data, _ = get_data(dataset_path + file, n=rows_test)
        read_data = read_data.values.tolist()
        actual_data[name_file] = [ list(map(str, data)) for data in read_data ] 

    end = time.time()
    print('Tempo de leitura de dados:', (end-start) , 'segundos')
    return schema, data, training_data, actual_data

def send_cache(schema, training_data, actual_data, host, mounting=True):
    return RedisStream(schema, training_data, actual_data, host=host, mounting=mounting)
