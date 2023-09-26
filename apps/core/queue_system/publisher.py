import json
import os

import pika

BROKER_URL = "amqps://qiqdvcyl:KPtRQ1jnfpuF7NNuAaVi9tynarNPc6XH@hummingbird.rmq.cloudamqp.com/qiqdvcyl"

class BasePublisher(object):
    def __init__(self, routing_key, body) -> None:
        self.exchange = "test_exchange"
        self.queue = "test_queue"
        self.routing_key = routing_key
        self.url = BROKER_URL
        self.body = body

    
    def run(self):
        self.__start_connection()
        self.__publish_message()


    def __start_connection(self):
        params = pika.URLParameters(self.url)
        connection = pika.BlockingConnection(params)
        channel = connection.channel()

        channel.exchange_declare(self.exchange)
        channel.queue_declare(self.queue)
        channel.queue_bind(self.queue, self.exchange, self.routing_key)
        return channel, connection
    
    
    def __publish_message(self):
        channel, connection = self.__start_connection()
        channel.basic_publish(
            body=json.dumps(self.body),
            exchange=self.exchange,
            routing_key=self.routing_key
        )
        channel.close()
        connection.close()