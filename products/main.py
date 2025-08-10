from contextlib import asynccontextmanager

import uvicorn
from fastapi import FastAPI, Body, Depends, status, HTTPException
from fastapi.responses import JSONResponse, FileResponse
from sqlalchemy.orm import Session

from libs import database
from libs.logs import product_logger, action_with_logging
from models import product_request, product
from models.product import Product, ProductResponse
from models.product_request import ProductChangeRequest


@asynccontextmanager
async def lifespan(app: FastAPI):
    database.init_tables()
    yield


app = FastAPI(lifespan=lifespan)


@app.get("/products/info")
@action_with_logging
async def main():
    return FileResponse("html/index.html")


@app.post("/products/new")
@action_with_logging
async def create_product(new_product: ProductChangeRequest,
                         session: Session = Depends(database.get_session)):
    product_logger.info('New product created: {0} {1}'.format(new_product.new_name, new_product.new_price))
    new_product = product.create_product_object(new_product.new_name, new_product.new_price)
    session.add(new_product)
    session.commit()
    return ProductResponse(new_product)


@app.get("/products/{product_id}")
@action_with_logging
async def get_product(product_id: int,
                      session: Session = Depends(database.get_session)):
    product_response = session.get(Product, product_id)
    if product_response is None:
        raise HTTPException(status_code=404, detail="Product not found")
    else:
        return ProductResponse(product_response)


@app.put("/products/{product_id}")
@action_with_logging
async def update_product(product_id: int, new_product: ProductChangeRequest,
                         session: Session = Depends(database.get_session)):
    requested_product: Product = session.get(Product, product_id)
    if requested_product is None:
        raise HTTPException(status_code=404, detail="Product not found")
    else:
        product_logger.info(
            f'upadting product {product_id} to {new_product.new_name, new_product.new_price}')
        requested_product.name = new_product.new_name
        requested_product.price = new_product.new_price
        session.commit()
        return ProductResponse(requested_product)


@app.delete("/products/delete/{product_id}")
@action_with_logging
async def get_products(product_id: int, session: Session = Depends(database.get_session)):
    requested_product: Product = session.get(Product, product_id)
    if requested_product is None:
        raise HTTPException(status_code=404, detail="Product not found")
    else:
        product_logger.info(f'deleting product {product_id}')
        session.delete(requested_product)
        session.commit()
        return ProductResponse(requested_product)


@app.get("/products")
@action_with_logging
async def get_products(session: Session = Depends(database.get_session)):
    products = session.query(Product).all()
    products = list(map(ProductResponse, products))
    return products


if __name__ == "__main__":
    uvicorn.run(app, host="0.0.0.0", port=8001)
