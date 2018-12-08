install: venv setup

venv:
	virtualenv venv
	venv/bin/pip install -r requirements.txt

gather:
	venv/bin/python speed.py

server:
	venv/bin/python app.py
