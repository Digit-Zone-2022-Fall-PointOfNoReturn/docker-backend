# Django Backend Api
## Stores application
### GET `/api/stores/`
#### 200
##### JSON
```json
[
    {
        "id": uuid,
        "name": str,
        "address": str
    }
]
```

-----

### POST `/api/stores/`
#### PAYLOAD
```json
{
    "name": str,
    "address": str
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
When `name` or `address` are not represented.

-----

### GET `/api/stores/<uuid>`
#### 200
##### JSON
```json
{
    "id": uuid,
    "name": str,
    "address": str
}
```

#### 404

-----

### PUT `/api/stores/<uuid>`
#### 200
##### JSON
```json
{
    "name": str,
    "address": str
}
```

#### 400
When `name` or `address` are not represented.

#### 404

-----

### DELETE `/api/stores/<uuid>`
#### 200
#### 404

-----

### GET `/api/stores/<uuid>/products/`
#### 200
##### JSON
```json
[
    {
        "id": uuid,
        "name": str,
        "description": str,
        "price": str,  // Decimal 7.2
        "discount": json
    }
]
```

For now discount can be like this:
```json
{
    // ...
    "discount":
    {
        "type": "per",
        "step": 1
    }
}
```

**WARNING**: `"discount"` field is just an JSON. It doesn't influence on backend. So you need to evaluate all discounts manually

#### 404

-----

### POST `/api/stores/<uuid>/products/`
#### PAYLOAD
```json
{
    "name": str,
    "description": str,
    "price": str,  // Decimal 7.2
    "discount": json
}
```

#### 200
#### 400
When `PAYLOAD` is incomplete.

#### 404

-------

### GET `/api/stores/<uuid>/products/<uuid>`
#### 200
##### JSON
```json
{
    "id": uuid,
    "name": str,
    "description": str,
    "price": str,  // Decimal 7.2
    "discount": json
}
```

#### 404

-----

### DELETE `/api/stores/<uuid>/products/<uuid>`
#### 200
#### 404

----

### PUT ` /api/stores/<uuid>/products/<uuid>`
#### PAYLOAD
```json
{
    "name": str,
    "description": str,
    "price": str,  // Decimal 7.2
    "discount": json
}
```

#### 200
#### 400
When `PAYLOAD` is incomplete.

#### 404
