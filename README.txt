recommended: install poetry
see https://python-poetry.org/docs/#installation

or `curl -sSL https://install.python-poetry.org | python3 -`

1. install libs from pyproject.toml
`poetry install`
2. run with python 3.7+
``python3 PhotoOrganier.py`

how to create exe and dmg
3. run "pyinstaller PhotoOrganizer.spec" in the venv using `poetry run pyinstaller PhotoOrganizer.spec`

Deployed fine in windows
but on mac:
can't build.
see https://www.pythonguis.com/tutorials/packaging-pyqt5-applications-pyinstaller-macos-dmg/ on how you could generate a dmg


TODO:
- pyside6-uic needs to be in path, can be replaced by programmatically including the .ui files or generating them beforehand.
- *.ui files need to be included in pyinstaller, is very cumbersome
-> this means, use QUILoader instead of loadUiType()
- check if every function works
  - photographer can select two paths
  - photos get moved into respective client folders which are created using the client number found in the qr code
  - see 'sample pics for testing' to test the code

- please put ressources into folders, ui files into folders
- please make sure to create a .dmg file 
