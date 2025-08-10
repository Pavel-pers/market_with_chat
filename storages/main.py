from contextlib import asynccontextmanager
from typing import cast

import uvicorn
from fastapi import FastAPI, Depends, HTTPException, Body
from sqlalchemy import select
from sqlalchemy.orm import Session
import requests

from libs import database
from libs.logs import storage_logger, action_with_logging
from models.storage import Storage, StorageResponce, create_storage_object
from models.product_quantity import ProductQuantity, ProductQuantityResponce
from models.product_quantity_difference import ProductQuantityDifference
from resources import constants


@asynccontextmanager
async def lifespan(app: FastAPI):
    database.init_tables()
    yield


app = FastAPI(lifespan=lifespan)


@app.post("/storages/create")
@action_with_logging
async def create_storage(new_storage_name: str, session: Session = Depends(database.get_session)):
    storage_logger.info("Creating new storages %s", new_storage_name)
    new_storage = create_storage_object(new_storage_name)
    session.add(new_storage)
    session.commit()
    return StorageResponce(new_storage)


@app.delete("/storages/delete")
@action_with_logging
async def delete_storage(storage_id: int, session: Session = Depends(database.get_session)):
    requested_storage = session.get(Storage, storage_id)
    if requested_storage is None:
        raise HTTPException(status_code=404, detail="Storage not found")
    else:
        products_in_storage = session.execute(select(ProductQuantity).where(
            cast("ColumnElement[bool]",
                 ProductQuantity.storage_id == storage_id)
        ))

        for product in products_in_storage:
            product = product[0]
            storage_logger.info(f"Deleting product {product.product_id} from storages {storage_id}")
            session.delete(product)

        storage_logger.info(f"Deleting storages {storage_id}")
        session.delete(requested_storage)
        session.commit()
        return StorageResponce(requested_storage)


@app.get("/storages/")
@action_with_logging
async def get_storages(session: Session = Depends(database.get_session)):
    storages = session.query(Storage).all()
    storages = list(map(StorageResponce, storages))
    return storages


@app.post("/storages/{storage_id}")
@action_with_logging
async def update_storage_info(storage_id: int, products_difference: list[ProductQuantityDifference] = Body(embed=True),
                              session: Session = Depends(database.get_session)):
    requested_storage = session.get(Storage, storage_id)
    if requested_storage is None:
        raise HTTPException(status_code=404, detail="Storage not found")
    else:
        products_in_storage = []
        products_to_create = []
        for product_diff in products_difference:
            if not is_product_in_db(product_diff.product_id, session):
                raise HTTPException(status_code=404, detail="Product not found")
            product_row: ProductQuantity | None = session.execute(select(ProductQuantity).
            where(ProductQuantity.storage_id == storage_id).
            where(
                ProductQuantity.product_id == product_diff.product_id)).first()
            if product_row is None:
                if product_diff.difference < 0:
                    raise HTTPException(status_code=401, detail="Product quantity out of range")
                else:
                    products_to_create.append(product_diff)  # make it after because of exceptions
                    continue
            else:
                product_row = product_row[0]

            if product_row.quantity + product_diff.difference < 0:
                raise HTTPException(status_code=401, detail="Product quantity out of range")
            else:
                product_row.quantity += product_diff.difference
                if product_row.quantity == 0:
                    session.delete(product_row)
                else:
                    products_in_storage.append(ProductQuantityResponce(product_row))

        for product in products_to_create:
            session.add(ProductQuantity(storage_id, product.product_id, product.difference))
            product_quantity = ProductQuantity(storage_id, product.product_id, product.difference)
            products_in_storage.append(ProductQuantityResponce(product_quantity))
        session.commit()

        session.commit()
        return products_in_storage


@app.post("/storages/update_one/{storage_id}-{product_id}")
@action_with_logging
def update_storage_info_one_product(storage_id: int, product_id: int, difference: int,
                                    session: Session = Depends(database.get_session)):
    quantity_request = ProductQuantityDifference(product_id=product_id, difference=difference)
    return update_storage_info(storage_id, [quantity_request], session=session)


@app.get("/storages/{storage_id}")
@action_with_logging
async def get_product_quantity_by_storage(storage_id: int, session: Session = Depends(database.get_session)):
    products_in_storage = session.execute(select(ProductQuantity).where(
        cast("ColumnElement[bool]",
             ProductQuantity.storage_id == storage_id)
    ))

    products = session.execute(select(ProductQuantity).where(
        cast("ColumnElement[bool]",
             ProductQuantity.storage_id == storage_id)
    )).all()

    products_responce = list(map(
        lambda item: ProductQuantityResponce(item[0]), products))
    return products_responce


def is_product_in_db(product_id: int, session: Session):
    return requests.get(constants.PRODUCTS_URL + f'/products/{product_id}').ok


if __name__ == "__main__":
    uvicorn.run(app, host="0.0.0.0", port=8000)
