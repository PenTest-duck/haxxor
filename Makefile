build:
	docker build -t haxxor .

run:
	docker run $(DOCKER_FLAGS) \
	haxxor \
	uv run /app/src/main.py --target=$(target) --connection=$(connection) --model=$(model)

run-local:
	uv run src/main.py --target=$(target) --connection=$(connection) --model=$(model)

run-shell:
	docker run $(DOCKER_FLAGS) \
	--entrypoint /bin/bash \
	haxxor

DOCKER_FLAGS = -it \
	--env-file .env \
	-e PYTHONUNBUFFERED=1 \
	-e PYTHONDONTWRITEBYTECODE=1 \
	-v $(PWD)/src:/app/src \
	-v $(PWD)/connections:/app/connections \
	-v $(PWD)/logs:/app/logs \
	-v $(PWD)/pyproject.toml:/app/pyproject.toml \
	-v $(PWD)/uv.lock:/app/uv.lock \
	--cap-add=NET_ADMIN \
	--device /dev/net/tun \
	--sysctl net.ipv6.conf.all.disable_ipv6=0
