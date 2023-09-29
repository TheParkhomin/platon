-include .env

run:
	@uvicorn platon_service.server --host=0.0.0.0 --reload

docker.compose.run:
	@docker compose run -p 8000:8000 service

db.migrate:
	@yoyo apply --database ${DB_URL} -b ./migrations

db.rollback:
	@yoyo rollback --database ${DB_URL} -b

test:
	@pytest