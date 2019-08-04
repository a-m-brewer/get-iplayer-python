#!/usr/bin/env bash
python3 setup.py sdist
python3 setup.py bdist_wheel --universal
python3 -m twine upload dist/* -r private
