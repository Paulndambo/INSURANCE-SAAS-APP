import json
import pika, os
from apps.queue_system import settings

url = os.environ.get('CLOUDAMQ_URL', 'amqp://guest:guest@localhost:5672/')

class BaseConsumer(object):
    exchange_name = "main_exchange" #settings.QUEUE_SETTINGS['EXCHANGE_NAME']
    exchange_type = "topic" #settings.QUEUE_SETTINGS['EXCHANGE_TYPE']
    queue_name = "main_queue" #settings.QUEUE_SETTINGS['QUEUE_NAME']
    consumer_name = None

    def __init__(self):
        pass


    def __base_consume(self):
        self.channel.basic_consume(self.__callback, queue=self.queue_name)
        self.channel.start_consuming()

    
    def __callback(self, ch, method, properties, body):
        try:
            body = json.loads(body.decode('utf-8'))
        except json.decoder.JSONDecodeError:
            return False

        try:
            settings.ROUTING_KEYS[self.consumer_name][method.routing_key]
        except KeyError:
            return False

    def __make_connection(self):
        """
        Make connection with RabbitMQ Server
        :return:
        """

        #credentials = pika.PlainCredentials(site_settings.RABBIT_MQ_USERNAME, site_settings.RABBIT_MQ_PASSWORD)
        #parameters = pika.ConnectionParameters(site_settings.RABBIT_MQ_HOST, 5672, '/', credentials)

        #self.connection = pika.BlockingConnection(parameters)
        params = pika.URLParameters(url)
        self.connection = pika.BlockingConnection(parameters=params)
        self.channel = self.connection.channel()

    def __queue_declare(self):
        self.channel.queue_declare(queue=self.queue_name, auto_delete=True)

    def __exchange_declare(self):
        self.channel.exchange_declare(
            exchange=self.exchange_name, exchange_type=self.exchange_type)

    def __queue_bind(self):
        try:
            settings.ROUTING_KEYS[self.consumer_name]
        except KeyError:
            return

        for key in settings.ROUTING_KEYS[self.consumer_name]:
    
            self.channel.queue_bind(
                exchange=self.exchange_name, queue=self.queue_name, routing_key=key)
