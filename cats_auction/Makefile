run:
	python -m catsauction.wsgi

check:
	pylint catsauction && mypy catsauction

db-migrate:
	PYTHONPATH=. alembic upgrade head

db-add:
	PYTHONPATH=. alembic revision --autogenerate

db-undo:
	PYTHONPATH=. alembic downgrade -1

test:
	pytest --disable-pytest-warnings --cov=catsauction catsauction/tests

-include Makefile.local
