QUEUE_SETTINGS = {
    'EXCHANGE_NAME': 'default',
    'EXCHANGE_TYPE': 'topic',
    'QUEUE_NAME': 'c2s1',
}

ROUTING_KEYS = {
    'messages': {
        "notifications.hello_world": ["print_hello_world", ],
    }

}
