.PHONY: build build-rpm

VERSION=$(cat spice2wav/__init__.py | grep __version__ \
		| sed 's/__version__[[:space:]]\+=[[:space:]]\+' \
		| sed "s/'//g")

build:
	python setup.py bdist_wheel

build-rpm:
	python setup.py bdist_rpm
