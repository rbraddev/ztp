#! /usr/bin/env bash
set -e

celery -A celery worker -l info -n quest@rabbitmq