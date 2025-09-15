install:
	pip install --upgrade pip
	pip install -r requirements.txt

run:
	uvicorn app.main:app --reload

migrate:
	alembic upgrade head

makemigrations:
	alembic revision --autogenerate -m "$(name)"

test:
	pytest -v

lint:
	black .
	isort .
	flake8 .

dc-up:
	docker-compose up -d

dc-down:
	docker-compose down

dc-restart: dc-down dc-up
