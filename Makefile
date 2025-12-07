
.PHONY: venv deps init run test ci

PY?=python

venv:
	$(PY) -m venv .venv

deps:
	pip install -r requirements.txt

init:
	$(PY) scripts/init_db.py

run:
	uvicorn app.main:app --host 127.0.0.1 --port 8000

test:
	pytest -q

ci:
	mkdir -p EVIDENCE/S08
	pytest --junitxml=EVIDENCE/S08/test-report.xml -q

check-python-version:
	@python3 -c 'import sys; assert sys.version_info >= (3, 11), "Python 3.11+ required"'

ci-s06: check-python-version
	mkdir -p EVIDENCE/S06/logs
	python3 -m venv .venv
	.venv/bin/pip install -r requirements.txt
	.venv/bin/python scripts/init_db.py
	.venv/bin/pytest -q --junitxml=EVIDENCE/S06/test-report.xml --log-file=EVIDENCE/S06/logs/pytest.log