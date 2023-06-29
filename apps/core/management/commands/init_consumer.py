from django.core.management.base import BaseCommand
from apps.core.queue_system.consumer import BaseConsumer

class Command(BaseCommand, BaseConsumer):
    consumer_name = "messages"

    def __init__(self):
        super().__init__()
        self.init_consumer()


    def init_consumer(self):
        super().init_consumer()

    
    def handle(self, *args, **options):
        print(' [*] waiting for messages. To exit press CTRL+C')
        self.base_consume()