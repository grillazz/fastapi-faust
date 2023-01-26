# fastapi-faust

Example integration of [FastAPI](https://fastapi.tiangolo.com/) integration with [Faust - Python Stream Processing Fork](https://github.com/faust-streaming/faust)

This is a very opinionated example repository for a python backend API.
It is not a template as it contains a few things already as an example for how to build something from here.

This project [fastapi-faust-example](https://github.com/toh995/fastapi-faust-example) was originally created by [toh995](https://github.com/toh995/), this is a hard fork as I intend to deviate from the upstream - 
adding more opinion and changing a few things i.e. switch from  [Faust](https://github.com/robinhood/faust) to [Faust - Python Stream Processing Fork](https://github.com/faust-streaming/faust)


### How to Setup
To build , run and test and more ... use magic of make help to play with this project.
```shell
make help
```


### Test with cURL
```shell
curl -X 'POST' \
  'http://0.0.0.0:8080/greeting?from_name=Faust&to_name=World' \
  -H 'accept: application/json' \
  -d ''
```
and you get response
```shell
fastapi-faust-api-1        | INFO:     172.24.0.1:65078 - "POST /greeting?from_name=Faust&to_name=World HTTP/1.1" 200 OK
fastapi-faust-worker-1     | [2023-01-26 19:39:59,701] [1] [WARNING] Saluti veloci da Faust a World 
fastapi-faust-api-1        | INFO:     172.24.0.1:62310 - "POST /greeting?from_name=Faust&to_name=World HTTP/1.1" 200 OK
fastapi-faust-worker-1     | [2023-01-26 19:40:34,334] [1] [WARNING] Saluti veloci da Faust a World 
fastapi-faust-api-1        | INFO:     172.24.0.1:64476 - "POST /greeting?from_name=Faust&to_name=World HTTP/1.1" 200 OK
fastapi-faust-worker-1     | [2023-01-26 19:40:37,264] [1] [WARNING] Saluti veloci da Faust a World 
fastapi-faust-api-1        | INFO:     172.24.0.1:64478 - "POST /greeting?from_name=Faust&to_name=World HTTP/1.1" 200 OK
fastapi-faust-worker-1     | [2023-01-26 19:40:38,026] [1] [WARNING] Saluti veloci da Faust a World 

```

FastAPI + Faust = :heart:
