-include .env

run:
	@python -m platon_service

docker.compose.run:
	@docker compose run -p 8000:8000 service

db.migrate:
	@yoyo apply --database ${DB_URL} -b ./migrations

db.rollback:
	@yoyo rollback --database ${DB_URL} -b

test:
	@pytest

lint:
	@mypy platon_service
	@flake8 platon_service
