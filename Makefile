PY ?= python3
PIP ?= pip3
PORT ?= 8000
VENV ?= .venv

install:
	$(PY) -m venv $(VENV)
	$(VENV)/bin/pip install --upgrade pip
	$(VENV)/bin/pip install -r requirements.txt

run:
	$(VENV)/bin/uvicorn app.main:app --reload --host 0.0.0.0 --port $(PORT)

test:
	$(VENV)/bin/pytest -q

docker-build:
	docker build -t askadb/orchestrator-api:local .

docker-run:
	docker run --rm -p $(PORT):$(PORT) --env-file ../askadb-infra/.env askadb/orchestrator-api:local

