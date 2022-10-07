# Django Backend Api
## Users application
### GET `/api/users/?tag=<str>`
#### 200
##### JSON
```json
{
    "id": uuid,
    "tag": str,
    "name": str
}
```

#### 404

-----

### GET `/api/users/?name=<str>`
#### 200
##### JSON
```json
[
    {
        "id": uuid,
        "tag": str,
        "name": str
    }
]
```

#### 404

-----

### GET `/api/users/?name=<str>&tag=<tag>`
`name` ignored, same as `GET /api/users/?tag=<str>`

-----

### POST `/api/users/`
NOTE: In case when tag is not set, it will have `"-" + uuid4()` value. That neccessary because `Postgres 14` not allows to have `UNIQUE` values along with `NULL`.

#### PAYLOAD
```json
{
    "name": str,
    "tag": str  # OPTIONAL
}
```

#### 201
##### JSON
```json
{
    "id": uuid
}
```

#### 400
When `name` is not set

#### 409
When `tag` already exists

-----

### PUT `/api/users/<uuid>`
#### PAYLOAD I
```json
{
    "name": str
}
```

#### PAYLOAD II
```json
{
    "tag": str
}
```

#### 200
#### 400
When `PAYLOAD` is empty

#### 404

-----

### DELETE `/api/users/<uuid>`
#### 200
#### 404
