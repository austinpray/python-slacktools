.PHONY: build publish test

build:
	python setup.py sdist bdist_wheel

publish:
	twine upload dist/*
