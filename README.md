# Furniture Workshop 

This project is aimed to provide a simple backend for **TODO**

## API overview

### Category
- **GET '/api/category/list'** - returns all present categories

Example response body: 
```
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
```
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
        "description": "short_description_1"
    } 
]
``` 

- **GET /api/product/{productId}** - returns detailed info about requested product

Example response body: 
```
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