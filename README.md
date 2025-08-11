# Market realization project.

The project was created to study microservice architecture.

In project 3-4(?) microservices, and 4 databse tables.

## Microservices:

1. > **storages microservice**

(check if there is products in stock) on port: 8000
### features:
* add storage/market <- post method requires storage name, storage id generates automaticly
* get available storages <- get methos, returns list of Storage objects
* delete storage <- delete methos
* change quanity of products in storage <- put method requires storage id in url, and json of list dictionries that holds "part-id" and "product-quanity-differens" keys, *raise 404 if storage not found*
* change quanity of only one product <- put methos, makes same what previous, made becouse of lighter communication instead of list of dictionaries
* get quanity on one storage <- get method raise 404 if storage not found

2. > **product microservice**
   
 (work with name, price of product) on port 8001
### features:
 * add product <- post method
 * delete product <- delete methos 
 * change product  <- put methos
  **has his own index.html interface on products/info**

 3. > **client cart**
    
    (work with product cart of users) on port 8002
### features
  * add product to client-cart to definite storage <- post method requires user_id storage_id and json dict that holds "product_id", "quanity" keys, *raise 404 if storage or product doesnt exists*
  * get products in cart of user <- get method

4. > **root producer(in work)**
   
   (handle root page, has index.html, work with another microservices and combines data from them, for answer clients about cart information, and hold operations like buying product from cart)

    wotks on port 8003
