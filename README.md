# pyjigsaw
Python access to jigsaw

runs in Python 2.7

requires the requests library

if not installed already

pip install requests

Then edit params.py to include your path to your token and your
output data directory

(and add params.py to your .gitignore if you want)

to run tests (requires nose to be installed, pip install nose)

nosetests tests.py

To create a file of all people do

python api.py