from propan import PropanApp, RabbitBroker
from propan.fastapi import RabbitRouter

# broker = RabbitBroker('amqp://rabbit-user:1542@localhost:5672/rabbit-wallet-vhost')  # Укажите свои настройки RabbitMQ
#
# rabbit_app = PropanApp(broker)
router = RabbitRouter('amqp://rabbit-user:1542@localhost:5672/rabbit-wallet-vhost')


