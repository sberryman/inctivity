build:
	docker build -t inctivity/scripts_import_az:latest .

run:
	docker run \
		-it --rm \
		-v `pwd`:/app \
		-w /app \
		python:3-buster \
		/bin/bash

cache:
	docker run \
		-it --rm \
		-v `pwd`:/app \
		inctivity/scripts_import_az:latest \
		python \
		cache.py