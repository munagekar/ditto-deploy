DOCKER_REPO := munagekar/ditto-deploy
VERSION := 0.1.0
IMAGE := $(DOCKER_REPO):$(VERSION)


.PHONY: requirments build

requirements:
	poetry export --without-hashes --format=requirements.txt > requirements.txt


build:
	@DOCKER_BUILDKIT=1 docker build . -t $(IMAGE)

push: build
	docker push $(IMAGE)
