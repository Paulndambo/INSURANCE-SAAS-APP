import os, pika
url = os.environ.get('CLOUDAMQ_URL', 'amqp://guest:guest@localhost:5672/')
import json

class BasePublisher(object):

    exchange_name = "main_exchange"
    exchange_type = "topic"
    

    def __init__(self, routing_key, body):
        self.body = body
        self.routing_key = routing_key

        
        self.__make_connection()
        self.__exchange_declare()
        self.__basic_publish()
        

    def __basic_publish(self):
        body = json.dumps(self.body)
        self.channel.basic_publish(
            exchange=self.exchange_name,
            routing_key=self.routing_key,
            body=body
        )
        self.connection.close()
    
    def __make_connection(self):
        params = pika.URLParameters(url)
        self.connection = pika.BlockingConnection(parameters=params)
        self.channel = self.connection.channel()


    def __exchange_declare(self):
        self.channel.exchange_declare(
            exchange=self.exchange_name,
            exchange_type=self.exchange_type
        )