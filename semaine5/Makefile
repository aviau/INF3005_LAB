all: run

env: requirements.txt
	rm -rf env
	virtualenv -p /usr/bin/python3 env
	env/bin/pip install -r requirements.txt

.PHONY: run
run: env
	FLASK_APP=app.py FLASK_DEBUG=1 env/bin/flask run

.PHONY: check
check: env
	env/bin/pycodestyle --verbose --exclude=env,__pycache__ .

.PHONY: clean
clean:
	rm -rf env
	rm -f signups.txt
