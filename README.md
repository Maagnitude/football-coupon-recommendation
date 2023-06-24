# Just-another-recommendations-system

```
flask db init
```
```
flask db migrate -m "Initial migration"
```
```
flask db upgrade
```

## To run the consumer
```
python tasks.py
```

## To begin the app server
```
python app.py
```

## Fill the form to send data to the consumer


## To run the tests
```
python -m unittest discover tests
```

## Dockerization
```
docker-compose up
```
It creates 1 container for the app, 2 containers for the 2 consumers, and 1 container for RabbitMQ

## Producer sends to "localhost:5000/api/get_coupon" the user_info, and consumer receives a new coupon