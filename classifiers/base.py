import copy
import csv
import heapq
import time
import warnings
import numpy
import pandas
import concurrent.futures

from builtins import FutureWarning

from sklearn.decomposition import PCA
from sklearn.feature_selection import SelectKBest, f_classif
from sklearn.neighbors import LocalOutlierFactor


class ClassifierBase:

    def __init__(self, schema, minPts, pca_components):
        self.pca = None
        self.schema = schema
        self.minPts = minPts
        self.pca_components = pca_components

    def preprocessing_data(self, read_data):
        if not self.pca:
            self.pca = PCA(n_components=self.pca_components, whiten=True)
            principalComponents = self.pca.fit_transform(read_data.values)
        else:
            # pca = self.pca.fit(read_data.values)
            principalComponents = self.pca.transform(read_data.values)
        processed_data = pandas.DataFrame(data = principalComponents, columns = range(self.pca_components))
        return processed_data

    def find_columns(self, read_data, actual_data, max_features):
        # read_data_copy = copy.deepcopy(read_data)
        # columns = read_data_copy.columns.values.tolist()
        # read_data_copy['class'] = 'Normal'
        # attack = list(actual_data.keys())[-1]
        # actual_data_copy = copy.deepcopy(actual_data[attack])
        # actual_data_copy = pandas.DataFrame(actual_data_copy, columns=columns)
        # actual_data_copy['class'] = 'Attack'
        # data = pandas.concat([read_data_copy, actual_data_copy])
        # X = data.drop('class', axis=1).values
        # Y = data['class'].values
        # clf = SelectKBest(f_classif, k=max_features).fit(X,Y)
        # # clf = clf.fit(X, Y)
        # columns = data.columns[numpy.append(clf.get_support(), [False])]
        # return columns.values
        self.columns = ['MI_dir_L0.01_weight', 'MI_dir_L0.01_mean', 'H_L0.1_mean', 'H_L0.01_weight', 'H_L0.01_mean',
            'HH_jit_L5_mean', 'HH_jit_L3_mean', 'HH_jit_L1_mean', 'HH_jit_L0.1_mean', 'HH_jit_L0.01_mean']

    def preprocessing_training_data(self, read_data, actual_data):
        start = time.time()
        self.find_columns(read_data, actual_data, 10)
        processed_data = self.preprocessing_data(read_data[self.columns])
        
        warnings.simplefilter("ignore", FutureWarning)
        clf = LocalOutlierFactor(n_neighbors=self.minPts)
        labels = clf.fit_predict(processed_data).tolist()
        processed_data.drop([labels.index(out) for out in labels if out == -1])
        
        end = time.time()
        print('Preprocessing time:', (end-start) , 'seconds')
        return processed_data

    def offline(self, data, number_data, number_devices):
        start = time.time()
        self._offline(data, number_data, number_devices)
        end = time.time()
        print('Offline:', (end-start) , 'seconds')

    def _offline(self, data, number_data, number_devices):
        raise NotImplemented('Método a ser implementado')

    def run(self, cache):
        inicio_online = time.time()

        try:
            i = true_positive_count = false_positive_count = true_negative_count = false_negative_count = 0

            while cache.has_actual_stream():
                i += 1
                new_data = cache.get_actual_stream()
                array = new_data.decode('utf-8').split(';')
                array = list(map(float, array))
                dataframe = pandas.DataFrame([array], columns=self.schema)
                dataframe = self.preprocessing_data(dataframe[self.columns])
                cluster = self.modelo.find_closest_cluster(dataframe, self.modelo.micro_clusters)
                result = self.modelo.check_fit_in_cluster(dataframe, cluster)
                if cache.last_type == 'training_stream':
                    if result:
                        true_positive_count += 1
                    else:
                        false_negative_count += 1
                else:
                    if not result:
                        true_negative_count += 1
                    else:
                        false_positive_count += 1

            fim_online = time.time()
            print('Online', fim_online - inicio_online, "seconds")
            print('# samples:', i, "samples")
            print('Sample time:', (( fim_online - inicio_online )/ i) * 1000, "miliseconds" )

            tpr = (true_positive_count / i) * 100
            fpr = (false_positive_count / i) * 100
            tnr = (true_negative_count / i) * 100
            fnr = (false_negative_count / i) * 100
            results = [
                f'TP = {tpr:.2f}% ({true_positive_count})',
                f'FP = {fpr:.2f}% ({false_positive_count})',
                f'TN = {tnr:.2f}% ({true_negative_count})',
                f'FN = {fnr:.2f}% ({false_negative_count})',
                f'Accuracy = {tpr+tnr:.2f}% ({true_positive_count+true_negative_count})',
                f'Wrongs = {fpr+fnr:.2f}% ({false_positive_count+false_negative_count})'
            ]
            print(' | '.join(results))

        except Exception as e:
            print(e)

    def _run_async(self, new_data, last_type):
        '''
        true positive, false negative, true negative, false positive
        '''
        raise NotImplemented('Método a ser implementado')

    def run_async(self, cache):
        inicio_online = time.time()

        try:
            # Pool de execução para paralelismo (https://docs.python.org/3/library/concurrent.futures.html#threadpoolexecutor-example)
            with concurrent.futures.ThreadPoolExecutor() as executor:
                
                i = true_positive_count = false_positive_count = true_negative_count = false_negative_count = 0
                threads = {}
                while cache.has_actual_stream():
                    i += 1
                    new_data = cache.get_actual_stream()
                    last_type = cache.last_type
                    # registrando execução para o pool
                    threads[executor.submit(self._run_async, new_data, last_type, i)] = i
                # Assim que as threads tiverem resultado
                for future in concurrent.futures.as_completed(threads):
                    amostra = threads[future]
                    try:
                        results = future.result()
                    except Exception as exc:
                        raise exc
                        print(f'Problem with sample {amostra}.')
                    else:
                        true_positive_count += results[0]
                        false_negative_count += results[1]
                        true_negative_count += results[2]
                        false_positive_count += results[3]

            fim_online = time.time()
            print('Online', fim_online - inicio_online, "seconds")
            print('# samples:', i, "samples")
            print('Sample time:', (( fim_online - inicio_online )/ i) * 1000, "miliseconds" )

            tpr = (true_positive_count / i) * 100
            fpr = (false_positive_count / i) * 100
            tnr = (true_negative_count / i) * 100
            fnr = (false_negative_count / i) * 100
            results = [
                f'TP = {tpr:.2f}% ({true_positive_count})',
                f'FP = {fpr:.2f}% ({false_positive_count})',
                f'TN = {tnr:.2f}% ({true_negative_count})',
                f'FN = {fnr:.2f}% ({false_negative_count})',
                f'Accuracy = {tpr+tnr:.2f}% ({true_positive_count+true_negative_count})',
                f'Wrongs = {fpr+fnr:.2f}% ({false_positive_count+false_negative_count})'
            ]
            print(' | '.join(results))

        except Exception as e:
            print(e)
