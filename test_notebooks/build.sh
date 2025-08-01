#! /bin/bash

cd ../
python setup.py bdist_wheel
cp dist/OpenSpecimenAPIconnector-0.9.3-py3-none-any.whl ../os-datahandler/dep/OpenSpecimenAPIconnector-0.9.3-py3-none-any.whl
/home/christoph/git/os-datahandler/.venv/bin/python -m pip install --force-reinstall /home/christoph/git/os-datahandler/dep/OpenSpecimenAPIconnector-0.9.3-py3-none-any.whl
