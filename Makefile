
include .env
export

.PHONY: all run fmt test clean dev build-docker run-docker

LOCAL_TAG := count-von-count:local

dev:
	poetry run uvicorn count_von_count.main:create_app --factory --reload

build-docker:
	docker build \
		-t $(LOCAL_TAG) \
		--build-arg POETRY_VERSION="1.8.3" \
		--progress plain \
		"."

run-docker: build-docker
	docker run --rm -p 8000:8000 $(LOCAL_TAG)

fmt:
	poetry run isort .
	poetry run black .

test:
	poetry run pytest --memray .

clean:
	find . -type f -name '*.pyc' -delete
	find . -type d -name '__pycache__' -delete
