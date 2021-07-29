unittest:
	PYTHONPATH=. pytest -m unit tests/

release:
	rm -rf ./dist || exit 0
	python setup.py sdist
	twine upload dist/*
