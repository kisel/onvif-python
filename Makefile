image:
	docker build -t onvif .

run:
	docker run -i -t --rm --net=host onvif

