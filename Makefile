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

.PHONY: test deploy docker-image

lint:
	bash -c "source ${ROOT_DIR}/.venv/bin/activate && black --check owenscrape"

test: 
	bash -c "source ${ROOT_DIR}/.venv/bin/activate && pytest tests"

test-watch:
	bash -c "source ${ROOT_DIR}/.venv/bin/activate && ptw"

requirements: venv
	${ROOT_DIR}/.venv/bin/pip install -r ./requirements.txt
	${ROOT_DIR}/.venv/bin/pip install -r ./test-requirements.txt

venv:
	virtualenv -p python3 .venv
	.venv/bin/pip install -r ./requirements.txt

docker:
	docker build -t $(IMG) .
	docker tag ${IMG} ${LATEST}

tag:
	@echo ${TAG}
