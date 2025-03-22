build:
	docker build -t haxxor .

run:
	docker run \
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
	--sysctl net.ipv6.conf.all.disable_ipv6=0 \
	haxxor \
	/bin/bash -c "uv add psutil && uv run /app/src/main.py --target=$(target) --connection=$(connection)"
	# uv run /app/src/main.py --target=$(target) --connection=$(connection)

run-local:
	python3 src/main.py --target=$(target) --connection=$(connection)
