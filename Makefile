build:
	docker build -t haxxor .

run:
	docker run \
	--env-file .env \
	-e PYTHONUNBUFFERED=1 \
	-e PYTHONDONTWRITEBYTECODE=1 \
	-v $(PWD):/app \
	--cap-add=NET_ADMIN \
	--device /dev/net/tun \
	--sysctl net.ipv6.conf.all.disable_ipv6=0 \
	haxxor \
	python3 /app/src/main.py --target="10.10.10.245"