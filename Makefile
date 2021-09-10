all: build up

build: 	
	docker-compose build 

up:
	docker-compose up --remove-orphans

down:
	docker-compose down
