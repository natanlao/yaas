test:
	python -m unittest discover
	flake8 --ignore E501 --show-source --count --statistics *.py
	mypy *.py --ignore-missing-imports
