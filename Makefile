unittest:
	PYTHONPATH=. pytest -m unit tests/

release:
	python setup.py sdist
	twine upload dist/*
	rm -rf ./dist
