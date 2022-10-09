# Django Backend Api
## Stores application
### GET `/api/groups/?user=<int>`
#### 200
```json
[uuid]
```
#### 400
When `user` param is not set

-----

### POST `/api/groups/`
#### PAYLOAD
```json
{
    "name": str,
    "admin": unsigned int,
    "users": [unsigned int]
}
```

#### 201
##### JSON
```json
{
    "id": uuid
}
```

#### 404
When `admin` or one of `users` does not exist

-----

### DELETE `/api/groups/<uuid>`
#### 200
#### 404

-----

### GET `/api/groups/<uuid>`
#### 200
##### JSON
```json
{
    "id": uuid,
    "name": str,
    "admin": unsigned int,
    "store": uuid,
    "collecting": bool
}
```

#### 404

-----

### PUT `/api/groups/<uuid>`
#### PAYLOAD I
```json
{
    "name": str
}
```

#### PAYLOAD II
```json
{
    "admin": unsigned int
}
```

#### PAYLOAD III
```json
{
    "name": str,
    "admin": unsigned int
}
```

#### 200
#### 400
When `PAYLOAD` empty

#### 404

-----

### PUT `/api/groups/<uuid>/stores/<uuid>`
Sets current store to group

#### 200
#### 404
#### 409
Store is collecting now

-----

### DELETE `/api/groups/<uuid>/stores/<uuid>`
Set current store to none

#### 200
#### 404
#### 409
Store is collecting now

-----

### GET `/api/groups/<uuid>/stores/<uuid>/carts`
#### 200
##### JSON
```json
[
    {
        "group": uuid,
        "user": unsigned int,
        "store": uuid,
        "product": uuid,
        "amount": unsigned int  // 1, 2, 3 ...; 0 amount records must be removed by backend
    }
]
```

#### 404

-----

### POST `/api/groups/<uuid>/stores/start`
#### 200
#### 404
#### 409
Store is not set

-----

### POST `/api/groups/<uuid>/stores/stop`
#### 200
#### 404
#### 409
Store is not set

-----

### POST `/api/groups/<uuid>/stores/drop`
Also clear all carts of this group in current store

#### 200
#### 404
#### 409
Store is not set or collecting active

-----

### GET `/api/groups/<uuid>/users/`
#### 200
##### JSON
```json
[
    {
        "group": uuid,
        "user": unsigned int,
    }
]
```

#### 404

-----

### DELETE `/api/groups/<uuid>/users/<unsigned int>`
#### 200
#### 404

-----

### POST `/api/groups/<uuid>/users/<unsigned int>`
#### 200
#### 404

-----

### DELETE `/api/groups/<uuid>/users/<unsigned int>/stores/<uuid>/cart`
Flushes cart content

#### 200

-----

### GET `/api/groups/<uuid>/users/<unsigned int>/stores/<uuid>/cart`
#### 200
##### JSON
```json
[
    {
        "group": uuid,
        "user": unsigned int,
        "store": uuid,
        "product": uuid,
        "amount": unsigned int
    }
]
```

-----

### DELETE `/api/groups/<uuid>/users/<unsigned int>/stores/<uuid>/product/<uuid>/cart`
#### PAYLOAD
```json
{
    "amount": unsigned int  // OPTIONAL, DEFAULT 1
}
```

#### 200
#### 400
When group store is not that in url (or not set in db)

#### 404
#### 409
When collecting is not started or store is wrong

-----

### PUT `/api/groups/<uuid>/users/<unsigned int>/stores/<uuid>/product/<uuid>/cart`
#### PAYLOAD
```json
{
    "amount": unsigned int  // OPTIONAL, DEFAULT 1
}
```

#### 200
#### 400
When group store is not that in url (or not set in db)

#### 404
#### 409
When collecting is not started or store is wrong
