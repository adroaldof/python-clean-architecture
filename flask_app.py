"""Flask APP API"""
from flask import Flask, request
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

import orm
from config import get_postgres_uri
from model import OrderItem, OutOfStock
from repository import StockBatchRepositoryAdapter
from services import allocate

orm.start_mappers()
get_session = sessionmaker(bind=create_engine(get_postgres_uri()))

app = Flask(__name__)


@app.route("/", methods=["GET"])
def root_endpoint():
    return ({"ping": "pong"}, 200)


@app.route("/healthz", methods=["GET"])
def healthz_endpoint():
    return ("", 200)


@app.route("/allocate", methods=["POST"])
def allocate_endpoint():
    session = get_session()
    repository = StockBatchRepositoryAdapter(session)

    params = request.json

    item = OrderItem(
        params["order_id"],
        params["sku"],
        params["quantity"],
    )

    try:
        batch_reference = allocate(item, repository, session)

        return ({"reference": batch_reference}, 201)
    except (OutOfStock) as error:
        return ({"message": str(error)}, 400)
