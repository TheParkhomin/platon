-include .env

run:
	@uvicorn platon_service.server --host=0.0.0.0 --reload

db.migrate:
	@yoyo apply --database ${DB_URL} -b ./migrations

db.rollback:
	@yoyo rollback --database ${DB_URL} -b
