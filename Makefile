
include .env
export

.PHONY: download-test test-upload fmt test clean dev build-docker run-docker install

LOCAL_TAG := count-von-count:local
WORK_DIR := $(shell pwd)

download-test:
	mkdir -p data
	curl --output data/test.pdf https://www.saffm.hq.af.mil/Portals/84/documents/FY25/FY25%20Air%20Force%20Working%20Capital%20Fund.pdf?ver=sHG_i4Lg0IGZBCHxgPY01g%3d%3d
	echo 'TEST_FILE=$(WORK_DIR)/data/test.pdf' > .env


test-upload:
	curl http://localhost:8000/api/v1/count/ -F "file=@$(WORK_DIR)/data/fy25_air_force_working_capital_fund.pdf"

install:
	poetry install
	poetry run python -m spacy download en_core_web_sm

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
