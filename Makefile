
include .env
export

.PHONY: all run fmt test clean docker-up docker-down
# Citation for the following code:
# Date: 04/06/2023
# Copied from /OR/ Adapted from /OR/ Based on:
# https://fastapi.tiangolo.com/deployment/server-workers/#run-gunicorn-with-uvicorn-workers
# and
# https://stackoverflow.com/questions/25319690/how-do-i-run-a-flask-app-in-gunicorn-if-i-used-the-application-factory-pattern
# NOTE: don't run this locally with that 0.0.0.0 bind
run:
	poetry run gunicorn "count_von_count.main:create_app()" --workers 4 --worker-class uvicorn.workers.UvicornWorker \
	--bind 0.0.0.0:8675 --capture-output \
	--access-logfile ${WEB_SERVER_ACCESS_LOGFILE} --error-logfile ${WEB_SERVER_ERROR_LOGFILE} \
	-D

dev:
	poetry run uvicorn count_von_count.main:create_app --factory --reload

fmt:
	poetry run isort .
	poetry run black .

test:
	poetry run pytest --memray .

clean:
	find . -type f -name '*.pyc' -delete
	find . -type d -name '__pycache__' -delete
