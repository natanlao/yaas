test:
	python -m unittest discover
	flake8 --max-line-length=120 --show-source --count --statistics *.py
	mypy *.py --ignore-missing-imports
