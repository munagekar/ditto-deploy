DOCKER_REPO := munagekar/ditto-deploy
VERSION := 0.1.7
IMAGE := $(DOCKER_REPO):$(VERSION)


.PHONY: requirments
.PHONY: build push
.PHONY: fmt lint

requirements:
	poetry export --without-hashes --format=requirements.txt > requirements.txt


build:
	docker buildx build --platform linux/amd64 . -t $(IMAGE)

push: build
	docker push $(IMAGE)

fmt:
	poetry run python -m isort . && \
	poetry run python -m black .

lint:
	poetry run python -m mypy . && \
	poetry run python -m flake8 ditto_deploy && \
	poetry run python -m black --check . && \
	poetry run python -m isort --check .

