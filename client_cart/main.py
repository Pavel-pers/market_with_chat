from contextlib import asynccontextmanager

import uvicorn
from fastapi import FastAPI, Body, Depends, HTTPException
from sqlalchemy.orm import Session
from sqlalchemy import select
import requests

from libs.logs import action_with_logging
from libs import database
from models.clientCartPositionsRequest import ClientCartPositionsRequest
from models.clientCartPositions import ClientCartPositions, ClientCartPositionsResponce
from libs.logs import client_cart_logger
from resources import constants

@asynccontextmanager
async def lifespan(app: FastAPI):
    database.init_tables()
    yield


app = FastAPI(lifespan=lifespan)


@app.post("/cart/{client_id}/{storage_id}")
@action_with_logging
async def create_position(client_id: int, storage_id: int,
                          cartPositionDifference: ClientCartPositionsRequest = Body(embed=True),
                          session: Session = Depends(database.get_session)):
    if not is_storage_exists(storage_id):
        raise HTTPException(status_code=404, detail="Storage does not exist")
    elif not is_product_exists(cartPositionDifference.product_id):
        raise HTTPException(status_code=404, detail="Product does not exist")
    else:
        client_cart_logger.info(
            f"Creating client cart position {client_id}/{storage_id} {cartPositionDifference.product_id} with quantity {cartPositionDifference.quantity}")

        requested_position = session.execute(
            select(ClientCartPositions).where(ClientCartPositions.client_id == client_id).where(
                ClientCartPositions.storage_id == storage_id).where(
                ClientCartPositions.product_id == cartPositionDifference.product_id)).first()

        if requested_position is None:
            new_position = ClientCartPositions(client_id=client_id,
                                               storage_id=storage_id,
                                               product_id=cartPositionDifference.product_id,
                                               quantity=cartPositionDifference.quantity)
            requested_position = new_position
            session.add(new_position)
        else:
            requested_position = requested_position[0]
            requested_position.quantity += cartPositionDifference.quantity
        session.commit()
        return requested_position


@app.get("/cart/{client_id}/{storage_id}")
@action_with_logging
async def get_positions(client_id: int, storage_id: int, session: Session = Depends(database.get_session)):
    if not is_storage_exists(storage_id):
        raise HTTPException(status_code=404, detail="Storage does not exist")
    else:
        requested_positions = (session.query(ClientCartPositions).
                               filter(ClientCartPositions.client_id == client_id).
                               filter(ClientCartPositions.storage_id == storage_id).all())
        requested_positions = list(
            map(lambda row: ClientCartPositionsResponce(row.client_id, row.storage_id, row.product_id, row.quantity),
                requested_positions))
        return requested_positions

def is_storage_exists(storage_id: int):
    return requests.get(constants.STORAGES_URL + f'/storages/{storage_id}').ok

def is_product_exists(product_id: int):
    return requests.get(constants.PRODUCTS_URL + f'/products/{product_id}').ok

if __name__ == "__main__":
    uvicorn.run(app, host="0.0.0.0", port=8002)
