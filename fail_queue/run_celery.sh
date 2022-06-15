# rabbitmqctl add_vhost qa1
# celery -A tasks purge -f
celery -A tasks worker -l info -c 4