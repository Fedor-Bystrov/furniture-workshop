# workshop-api 

This project is aimed to provide a simple backend for **TODO**

## Create and run application

In order to run application, *docker* and *docker-compose* have to be installed

`> docker-compose up -d --build`

`> curl localhost:3130/api/product/list`

## API overview

### Category
- **GET '/api/category/list'** - returns all present categories

Example response body: 
```json
[
  {
    "categoryId": 1,
    "name": "category_name_1"
  },
  {
    "categoryId": 2,
    "name": "category_name_2"
  },
  {
    "categoryId": 3,
    "name": "category_name_3"
  }
]
``` 

### Product
- **GET /api/product/list** - returns all present products

Example response body: 
```json
[
    {
        "productId": 1,
        "name": "product_name_1",
        "categoryId": 1,
        "description": "short_description_1"
    },
    {
        "productId": 2,
        "name": "product_name_2",
        "categoryId": 2,
        "description": "short_description_2"
    } 
]
``` 

- **GET /api/product/{productId}** - returns detailed info about requested product

Example response body: 
```json
{
    "productId": 1,
    "name": "product_name_1",
    "creationTime": "2018-09-04T19:28:32.527426",
    "category": {
        "categoryId": 1,
        "name": "category_name_1"
    },
    "price": "11.10",
    "description": "full_description_1"
}
```

### Cart
-  **GET /api/cart/{cartId}** 

Example response body: 
```json
{
    "cartId": 3,
    "creationTime": "2018-09-04T19:28:32.869403",
    "customer": {
        "customerId": 2,
        "creationTime": "2018-09-04T19:28:32.821221",
        "firstName": "first_name_2",
        "lastName": "last_name_2",
        "middleName": "middle_name_2",
        "locale": "ENG",
        "email": "test@test.com",
        "phone": "222222"
    },
    "price": "100000.00",
    "purchases": [
        {
            "productId": 7,
            "quantity": 17
        },
        {
            "productId": 2,
            "quantity": 15
        },
        {
            "productId": 6,
            "quantity": 10
        }
    ],
    "description": "description_3",
    "shippingAddress": "shipping_address_3"
}
```

- **POST /api/cart** - creates new cart

Example _request_ body (all fields, except _middleName_ are mandatory): 
```json
 {
  "firstName": "post_first_name_1",
  "lastName": "post_last_name_1",
  "middleName": "post_middle_name_1",
  "email": "post_test@test.com",
  "phone": "111111",
  "shippingAddress": "post_shipping_address_1",
  "purchases": [
    {
      "productId": 1,
      "quantity": 10
    },
    {
      "productId": 4,
      "quantity": 1
    },
    {
      "productId": 8,
      "quantity": 54
    }
  ],
  "price": "50001.01",
  "description": "post_description_1"
}
```

- **PUT /api/cart/{cartId}** updates existing cart with *id*

Example _request_ body (all fields except _purchases_ are optional):
```json
 {
  "firstName": "test_customer_first_name_1",
  "lastName": "test_customer_last_name_1",
  "middleName": "middle_name_1",
  "email": "put_test@test.com",
  "phone": "111111",
  "shippingAddress": "shipping_address_1",
  "purchases": [
    {
      "productId": 1,
      "quantity": 10
    },
    {
      "productId": 4,
      "quantity": 1
    },
    {
      "productId": 8,
      "quantity": 54
    }
  ],
  "price": "51",
  "description": "put_description_1"
}
```
