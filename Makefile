DOCKER_REPO := munagekar/ditto-deploy
VERSION := 0.1.1
IMAGE := $(DOCKER_REPO):$(VERSION)


.PHONY: requirments
.PHONY: build push
.PHONY: fmt lint

requirements:
	poetry export --without-hashes --format=requirements.txt > requirements.txt


build:
	@DOCKER_BUILDKIT=1 docker build . -t $(IMAGE)

push: build
	docker push $(IMAGE)

fmt:
	poetry run python -m isort . && \
	poetry run python -m black .

lint:
	poetry run python -m mypy ditto_deploy && \
	poetry run python -m flake8 ditto_deploy && \
	poetry run python -m black --check . && \
	poetry run python -m isort --check .

