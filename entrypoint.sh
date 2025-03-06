#!/bin/bash

set -e

wait_for_port() {
  local host="$1"
  local port="$2"
  local timeout=30
  local start_time=$(date +%s)

  local nc_command="nc"
  type $nc_command >/dev/null 2>&1 || nc_command="ncat"

  echo "Waiting for $host:$port..."
  while ! $nc_command -z "$host" "$port" >/dev/null 2>&1; do
    sleep 1
    local current_time=$(date +%s)
    local elapsed_time=$((current_time - start_time))

    if [ $elapsed_time -ge $timeout ]; then
      echo "ERROR: Service $host:$port unavailable after $timeout seconds"
      exit 1
    fi
  done
  echo "Service $host:$port is available"
}

wait_for_port "${DB_HOST:-postgres}" "${DB_PORT:-5432}"

python manage.py runserver 0.0.0.0:8000

#echo "Applying database migrations..."
#python manage.py migrate --noinput
#
#echo "Collecting static files..."
#python manage.py collectstatic --noinput
#
#echo "Starting Gunicorn server..."
#gunicorn core.config.wsgi:application --workers 3 --bind 0.0.0.0:8000
