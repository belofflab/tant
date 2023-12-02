build:
	docker build -t backend .
	docker run --name backend -v /var/www:/opt/backend/media -dp 8000:8000 backend
rebuild:
	docker kill backend
	docker rm /backend
	docker build -t backend .
	docker run --name backend -v /var/www:/opt/backend/media -dp 8000:8000 backend
upgrade:
	docker exec -t backend /opt/backend/venv/bin/alembic upgrade head
