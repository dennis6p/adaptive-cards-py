#! /usr/bin/bash

python3.10 -m build
python3 -m twine upload -r pypi dist/*

rm -r adaptive_cards_py.egg* dist