#!/bin/bash

# turn on bash's job control
set -m

# Start the primary process and put it in the background
if [ -z "$WORKER_CONTAINER" ]
then
    gunicorn --bind 0.0.0.0:9000 app.wsgi:application &
    nginx
    fg %1
else
    celery worker -A app -B --loglevel=debug --concurrency=4
fi