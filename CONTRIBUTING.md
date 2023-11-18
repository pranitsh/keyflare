

To run the tests and see the benchmarks:

```sh
pip install -e .[dev]
cd keyflare
pytest tests/
```

To test before you upload:
```sh
python -m venv env
# activate it
pip install -e .
```

To format the code before you upload:
```sh
pip install -e .[dev]
black .
pylint /keyflare
```

To build the package and upload:

```sh
# Make sure to delete dist/ if necessary
pip install -e .[dev]
python setup.py sdist bdist_wheel
twine upload dist/*
```

The current pylint score is 9.28. In pull requests, improvements to this score is appreciated.