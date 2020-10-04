import pandas,numpy
from sklearn.neighbors import LocalOutlierFactor

from denstream.denstream import DenStream
from denstream.sample import Sample

from .base import ClassifierBase

class DenStreamModel(ClassifierBase):

    def find_distance(self, data, include_self=False):
        LOF = LocalOutlierFactor(n_neighbors=self.minPts)
        LOF.fit(data)
        kdistgraph = LOF.kneighbors_graph(data, self.minPts, mode='distance')
        kdistgraph = kdistgraph.toarray()
        kdist = []
        for i in kdistgraph:
            medida = numpy.mean(i)
            kdist.append(medida)

        return kdist

    def find_eps(self, data):
        # 1. Calculate k-dist values of all point in dataset
        kdist = self.find_distance(data, self.minPts)    

        # 2. Sort the k-dist values and draw k-dist plot
        kdist.sort()

        # 3. Calculate slopes of each changes (or point) in k-dist plot
        slope_array=[]
        previous_value = kdist[0]
        for i in kdist:
            slope_array.append( i-previous_value )
            previous_value = i

        # 4. Calculate the mean and standard deviation of non-zero slopes.
        mean_slope = numpy.mean(slope_array)
        standard_deviation = numpy.std(slope_array)
        # print(mean_slope, standard_deviation)
        # pyplot.plot(slope_array)
        # pyplot.show()
        # print(f'Média: {mean_slope} | Desvio_padrão: {standard_deviation}')

        # 5. Find the first slope which is above mean(slope)+standard deviation(slope).
        # 6. Find corresponding k-dist value of the found slope in step 5 and assign this value as Eps.
        index = [ n for n,i in enumerate(slope_array) if i>(mean_slope+standard_deviation) ][0]
        # print(index)
        eps = kdist[index]

        # 7. Assign k as self.MinPts
        return eps

    def _offline(self,  data, number_data, number_devices):
        eps = self.find_eps(data)
        if number_data != 0:
            self.modelo = DenStream(lamb=0.03, epsilon=eps, minPts=self.minPts, mu='auto', startingBuffer=data.head(100))
        else:
            self.modelo = DenStream(lamb=0.03, epsilon=eps, minPts=self.minPts, mu='auto', startingBuffer=data)
        self.modelo.runInitialization()

    def _run_async(self, new_data, last_type, index):
        '''
        true positive, false negative, true negative, false positive
        '''
        array = new_data.decode('utf-8').split(';')
        array = list(map(float, array))
        dataframe = pandas.DataFrame([array], columns=self.schema)
        dataframe = self.preprocessing_data(dataframe[self.columns])
        sample = Sample(dataframe[0].values, index)
        result = self.modelo.runOnNewSample(sample)
        if last_type == 'training_stream':
            if not result:
                return 1,0,0,0
            else:
                return 0,1,0,0
        else:
            if result:
                return 0,0,1,0
            else:
                return 0,0,0,1
