## Start

- `docker-compose up`
- default admin user:
	- login: zeus
	- password: zeus


## API

#### POST `/api/login`

Privileges: anonymous

Request:
```
{
  "login": "zeus",
  "password": "zeus"
}
```

Response:
- HTTP 200 OK
- HTTP 400 Bad Request
- HTTP 401 Unauthorized

#### POST `api/logout`

Privileges: authorized

Response:
- HTTP 200 OK
- HTTP 401 Unauthorized

#### POST `/api/users/add`

Privileges: admin

Request:
```
{
  "login": "USER",
  "password": "PASSWORD"
}
```

Response:
- HTTP 200 OK
- HTTP 400 Bad Request
- HTTP 401 Unauthorized
- HTTP 500 Internal Server Error

#### POST `/api/posts/add`

Privileges: authorized

Request:
```
{
  "text": "TEXT",
  "tags": ["TAG", ..] [optional]
}
```

Response:
- HTTP 200 OK
- HTTP 400 Bad Request
- HTTP 401 Unauthorized
- HTTP 500 Internal Server Error

#### GET `/api/posts/my`

Privileges: authorized

Request:
- `?limit=LIMIT&tags=TAG1&tags=TAG2`
- limit=LIMIT [optional]
- tags=TAG .. [optional]

Response:
```
[
  {
    "date": "2019-12-07T16:08:54Z",
    "text": "TEXT",
    "tags": ["TAG", ..]
  },
  ..
]
```
- HTTP 200 OK
- HTTP 401 Unauthorized

#### GET `/api/posts/all`

Privileges: anonymous

Request:
- `?limit=LIMIT&tags=TAG1&tags=TAG2`
- limit=LIMIT [optional]
- tags=TAG .. [optional]

Response:
```
[
  {
    "user": "USER"
    "date": "2019-12-07T16:08:54Z",
    "text": "TEXT",
    "tags": ["TAG", ..]
  },
  ..
]
```
- HTTP 200 OK
- HTTP 401 Unauthorized
