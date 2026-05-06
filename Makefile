.PHONY: run bootstrap docker-run

run:
	uv run app

bootstrap:
	bash ./bootstrap.sh

docker-run:
	docker run --rm -p 8000:8000 \
	  --env-file .env \
	  -v $(CURDIR)/secrets:/app/secrets \
	  -v $(CURDIR)/maps:/app/maps \
	  -v $(CURDIR)/cache_data:/tmp/ndvi_cache \
	  ndvi_compare
