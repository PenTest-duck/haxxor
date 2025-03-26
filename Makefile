build:
	docker build -t haxxor .

run:
	docker run $(DOCKER_FLAGS) \
	-v $(PWD)/pyproject.toml:/app/pyproject.toml \
	-v $(PWD)/uv.lock:/app/uv.lock \
	haxxor \
	$(PYTHON_COMMAND) /app/src/main.py $(PYTHON_FLAGS)

run-local:
	$(PYTHON_COMMAND) src/main.py $(PYTHON_FLAGS)

run-shell:
	docker run $(DOCKER_FLAGS) \
	--entrypoint /bin/bash \
	haxxor

PYTHON_COMMAND = uv run

PYTHON_FLAGS = \
	--target=$(target) \
	--connection=$(connection) \
	--model=$(model) \
	--name=$(name)

DOCKER_FLAGS = \
	-it \
	--rm \
	--env-file .env \
	-e PYTHONUNBUFFERED=1 \
	-e PYTHONDONTWRITEBYTECODE=1 \
	-v $(PWD)/src:/app/src \
	-v $(PWD)/connections:/app/connections \
	-v $(PWD)/logs:/app/logs \
	--cap-add=NET_ADMIN \
	--device /dev/net/tun \
	--sysctl net.ipv6.conf.all.disable_ipv6=0
