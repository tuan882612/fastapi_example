.PHONY: start

NUM_CORES := $(shell python -c "import os; print(os.cpu_count())")
NUM_WORKERS := $(shell echo $$((2 * $(NUM_CORES) + 1)))

start:
	gunicorn src.main:app -b localhost:2000 -w $(NUM_WORKERS) -k uvicorn.workers.UvicornWorker
