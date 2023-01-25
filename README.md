# fastapi-faust

FastAPI + Faust = :heart:
ASGI fastapi integration with Python Stream Processing. A Faust fork with FastAPI integration.

## Basic Architecture
moved to confluence

## Running the app locally
This is a very opinionated example repository for a python backend API. It is not a template as it contains a few things already as an example for how to build something from here.
This project was originally created by grillazz, this is a hard fork as I intend to deviate from the upstream - adding more opinion and changing a few things.

dwa F F jedno czarne na zlieny drugie zielone na czarnym - piorun i piorko

# Build the container
```shell
    docker-compose build
```
# Run the container
```shell
    docker-compose up
```
docker-compose up

# Test with cURL
```shell
curl -X 'POST' 'http://0.0.0.0:8080/increment' -H 'accept: application/json' -d ''
```
and you get response
```shell
fastapi-faust-poc-api-1        | INFO:     172.18.0.1:57428 - "POST /increment HTTP/1.1" 200 OK
fastapi-faust-poc-worker-1     | [2022-12-23 12:05:13,105] [1] [WARNING] Hello from Faust to you 
fastapi-faust-poc-api-1        | INFO:     172.18.0.1:64008 - "POST /increment HTTP/1.1" 200 OK
fastapi-faust-poc-worker-1     | [2022-12-23 12:07:00,407] [1] [WARNING] Hello from Faust to you 
fastapi-faust-poc-api-1        | INFO:     172.18.0.1:58350 - "POST /increment HTTP/1.1" 200 OK
fastapi-faust-poc-worker-1     | [2022-12-23 12:07:07,233] [1] [WARNING] Hello from Faust to you 

```
