## Start

- `docker-compose up`
- db creds: see `docker-compose.yaml`
- web: `localhost:8080`
- 3 default users present with ids: 1, 2, 3

## API

#### POST `/v1/user/[USER_ID]/add-lot`

Request:
```
{
    "price": 10,
    "animal_id": 1
}
```

Response:
- HTTP 200 OK
- HTTP 400 Bad Request

#### POST `/v1/user/[USER_ID]/add-bet`

Request:
```
{
    "value": 10,
    "lot_id": 1
}
```

Response:
- HTTP 200 OK
- HTTP 400 Bad Request


#### POST `/v1/user/[USER_ID]/takes-bet`

Request:
```
{
    "bet_id": 1
}
```

Response:
- HTTP 200 OK
- HTTP 400 Bad Request
