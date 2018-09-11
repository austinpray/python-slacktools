.PHONY: build publish test test-all test-%

build:
	python setup.py sdist bdist_wheel

publish: build
	twine upload dist/*

test:
	${MAKE} test-3.7

test-all:
	${MAKE} test-3.7
	${MAKE} test-3.6
	${MAKE} test-3.5
	${MAKE} test-3.4

test-%:
	docker run --rm -v $(shell pwd):/app -w /app python:$(@:test-%=%) python setup.py test
