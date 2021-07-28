unittest:
	PYTHONPATH=. pytest -m unit

release:
	python setup.py sdist
	twine upload dist/*
	rm -rf ./dist
