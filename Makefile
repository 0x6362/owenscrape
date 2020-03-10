NAME         := 0x6362/owenscrape
TAG          := $(shell git rev-parse --short HEAD)
ifndef TAG
$(warning WARNING: Project must be a valid Git repository to enable image versioning. Defaulting version to 'latest'.)
TAG := latest
endif
IMG          := ${NAME}:${TAG}
LATEST       := ${NAME}:latest
GENERATE     := ${NAME}:generate
REGISTRY     := TBD
ROOT_DIR := $(shell dirname $(realpath $(lastword $(MAKEFILE_LIST))))

.PHONY: build-tools deploy docker-image

.venv:
	virtualenv -p python3 .venv
	.venv/bin/pip install -r ./requirements.txt

build-tools: \
	.venv

test-requirements: .venv
	.venv/bin/pip install -r ./test-requirements.txt

test: test-requirements
	bash -c "source .venv/bin/activate && pytest tests"

docker:
	docker build -t $(IMG) .
	docker tag ${IMG} ${LATEST}

tag:
	@echo ${TAG}
