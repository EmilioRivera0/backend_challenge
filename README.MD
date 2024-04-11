
# Back End Challenge API Reference


### UnitMeasures

#### Create a UnitMeasure element

```http
  POST /unitmeasures
```

| Parameter | Type     | Description                |
| :-------- | :------- | :------------------------- |
| `name` | `string` | **Required**. UnitMeasure's name |

#### Get all UnitMeasures

```http
  GET /unitmeasures
```

#### Get the specified UnitMeasure

```http
  GET /unitmeasures/<id>
```

| Parameter | Type     | Description                |
| :-------- | :------- | :------------------------- |
| `id` | `int` | **Required**. UnitMeasure's id |

#### Update a UnitMeasure element

```http
  PUT /unitmeasures
```

| Parameter | Type     | Description                |
| :-------- | :------- | :------------------------- |
| `id` | `int` | **Required**. UnitMeasure's id |
| `name` | `string` | **Required**. UnitMeasure's name |

#### Delete the specified UnitMeasure

```http
  DELETE /unitmeasures
```

| Parameter | Type     | Description                |
| :-------- | :------- | :------------------------- |
| `id` | `int` | **Required**. UnitMeasure's id |


### Products

#### Create a Product element

```http
  POST /products
```

| Parameter | Type     | Description                |
| :-------- | :------- | :------------------------- |
| `name` | `string` | **Required**. Product's name |
| `price` | `float` | **Required**. Product's price |
| `um_id` | `int` | **Required**. UnitMeasure's id |

#### Get all Products

```http
  GET /products
```

#### Get the specified Product

```http
  GET /products/<name>
```

| Parameter | Type     | Description                |
| :-------- | :------- | :------------------------- |
| `name` | `string` | **Required**. Product's name |

#### Update a Product element

```http
  PUT /products
```

| Parameter | Type     | Description                |
| :-------- | :------- | :------------------------- |
| `name` | `string` | **Required**. Product's name |
| `price` | `float` | **Required**. Product's price |
| `um_id` | `int` | **Required**. UnitMeasure's id |

#### Delete the specified Product

```http
  DELETE /products
```

| Parameter | Type     | Description                |
| :-------- | :------- | :------------------------- |
| `name` | `string` | **Required**. Product's name |


### Sales

#### Create a Sale element

```http
  POST /sales
```

| Parameter | Type     | Description                |
| :-------- | :------- | :------------------------- |
| `p_name` | `string` | **Required**. Product's name |
| `quantity` | `int` | **Required**. Quantity Sold |

#### Get the quantity and earned amount of each sold product

```http
  GET /sales
```

#### Get the quantity and earned amount of the specified product

```http
  GET /sales/<p_name>
```

| Parameter | Type     | Description                |
| :-------- | :------- | :------------------------- |
| `p_name` | `string` | **Required**. Product's name |

## Observations

- Sales table needs a primary key to be valid, so an ID column was added as the PK.
- Memory optimization can be achieved by relating Sales and Products through the Product ID instead of its name.
- PostgreSQL engine can perform the calculation of the quantity and amount sold from each product as well.
- AWS Lambda needs the psycopg2-binary package since it is a Linux instance.