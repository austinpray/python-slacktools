.PHONY: build publish test

build:
	python setup.py sdist bdist_wheel

publish: build
	twine upload dist/*
