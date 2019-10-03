@echo off
echo Creating python environment...
python -m venv venv

echo Entering python environment...
call venv/Scripts/activate

echo Installing requirements...
pip install setuptools wheel
pip install -r requirements.txt

echo Building mod-or-die...
rm -rf build/* && python setup.py sdist bdist_wheel && python setup.py build && python setup.py install
@echo on
