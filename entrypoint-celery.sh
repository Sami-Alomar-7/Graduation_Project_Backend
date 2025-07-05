#!/bin/bash

# Start Celery worker
celery -A graduation_backend worker --loglevel=info &

# Start Celery beat
celery -A graduation_backend beat --loglevel=info &

# Start Celery flower (monitoring)
celery -A graduation_backend flower --port=5555 --broker=redis://redis:6379/0