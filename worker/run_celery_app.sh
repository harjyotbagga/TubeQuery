celery -A tasks purge
celery -A tasks worker -l info -c 4 -Q tube_query_celery