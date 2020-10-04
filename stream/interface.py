from abc import ABC, abstractmethod
import random


class StreamInterface(ABC):

    broker = None
    training_stream = 'training_stream'
    last_type = None

    @abstractmethod
    def _mounting_data(self, queue, data):
        """
        Interface responsável por montar os dados que vão para o cache
        --
        Arguments:
        - queue: Nome da fila do dado
        - data: Lista com os parâmetros a serem adicionados
        """
        pass        

    @abstractmethod
    def _set_broker(self, host, port):
        """
        Interface responsável por setar a conexão principal, se houver, com o cache
        --
        Arguments:
        - host: Endereço do cache
        - port: Porta do cache
        """
        pass

    @abstractmethod
    def clean(self):
        """
        Interface responsável por setar a conexão principal, se houver, com o cache
        --
        Arguments:
        - host: Endereço do cache
        - port: Porta do cache
        """
        pass

    def __init__(self, schema, training_data, actual_data, host='localhost', port=6379, mounting=True):
        """
        Construtor da classe
        --
        Arguments:
        - schema: Estrutura dos dados
        - training_data: Matriz com os dados para treinamento (caso seja dados para serem enviados para o cache)
        - actual_data: Matriz com os dados para uso (caso seja dados para serem enviados para o cache)
        - host: Endereço do cache
        - port: Porta do cache
        - mounting: Boolean para enviar training_data e actual_data para o cache
        """
        self.broker = self._set_broker(host=host, port=port)
        self.schema = schema

        if mounting:
            # for line in training_data:
            self.types = [self.training_stream]
            self._mounting_data(self.training_stream, training_data)

            for option in actual_data:
                self.types.append(option)
                # for line in actual_data[option]:
                self._mounting_data(option, actual_data[option])

    @abstractmethod
    def _has_stream(self, option):
        """
        Interface responsável por verificar se existe dado para ser buscado no cache
        --
        Arguments:
        - option: Nome da fila
        """
        pass

    @abstractmethod
    def _get_stream(self, option):
        """
        Interface responsável por trazer dado do cache
        --
        Arguments:
        - option: Nome da fila
        """
        self.last_type = option
        if not self._has_stream(option):
            self.types.remove(option)
        pass

    def has_training_stream(self):
        """
        Método responsável por verificar se existe dado de treino para uso (Caso tenha sido utilizado mounting)
        --
        Arguments:
        - option: Nome da fila
        """
        return self._has_stream(self.training_stream)

    def get_training_stream(self):
        return self._get_stream(self.training_stream)
        
    def has_actual_stream(self):        
        return len(self.types) > 0

    def get_actual_stream(self):
        option = random.choice(self.types)
        return self._get_stream(option)
