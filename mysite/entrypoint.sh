#!/bin/bash

set -e

echo "Starting Django"

echo "Waiting DB..."
while ! nc -z course_db 5432; do
  sleep 1
done
echo "DB Done"

echo "Waiting Redis..."
while ! nc -z redis 6379; do
  sleep 1
done
echo "Redis is ready!"

if [[ "$1" == "web" || "$1" == "beat" ]]; then
  echo "Applying database migrations..."
  python manage.py migrate --noinput

  echo "Collecting static files..."
  python manage.py collectstatic --noinput --clear
fi

case "$1" in
  web)
    echo "Starting server Django"
    exec python manage.py runserver 0.0.0.0:8000
    ;;
  worker)
    echo "Starting Celery Worker"
    exec celery -A mysite worker --loglevel=info
    ;;
  beat)
    echo "Starting Celery Beat"
    exec celery -A mysite beat --loglevel=info
    ;;
  *)
    echo "Starting custom command"
    exec "$@"
    ;;
esac
