generate: venv

venv:
	virtualenv venv
	venv/bin/pip install -r requirements.txt

generate:
	venv/bin/python app.py

test:
	venv/bin/speedtest --csv >> speedtest.csv
