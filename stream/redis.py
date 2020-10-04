import redis, json
from .interface import StreamInterface


class RedisStream(StreamInterface):

    def _mounting_data(self, queue, data):
        obj = []
        for element in data:
            obj.append(';'.join(element))
        self.broker.rpush(queue, *obj)

    def clean(self):
        self.broker.flushall()

    def _set_broker(self, host, port):
        return redis.StrictRedis(host=host, port=port, db=0)    

    def _has_stream(self, option):
        return self.broker.llen(option) > 0

    def _get_stream(self, option):
        val = self.broker.lpop(option)
        super()._get_stream(option)
        return val

