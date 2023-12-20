.PHONY: start

NUM_CORES := $(shell python -c "import os; print(os.cpu_count())")
NUM_WORKERS := $(shell echo $$((2 * $(NUM_CORES) + 1)))

start:
	gunicorn src.main:app -b 0.0.0.0:2000 -w $(NUM_WORKERS) -k uvicorn.workers.UvicornWorker

reqs:
	pip freeze > requirements.txt

docker:
	docker build -t fastapi-app .
	docker run --env-file .env -p 2000:2000 fastapi-app
