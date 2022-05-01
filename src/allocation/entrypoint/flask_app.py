"""Flask APP API"""
from typing import Any, Dict

from flask import Flask, request
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

from allocation.adapters import orm
from allocation.adapters.stock_batch_adapter import StockBatchAdapter
from allocation.config import get_postgres_uri
from allocation.domain.order_item import OrderItem
from allocation.domain.out_of_stock_exception import OutOfStock
from allocation.service.services import allocate

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
    repository = StockBatchAdapter(session)

    params: Dict[str, Any] = request.json  # type: ignore

    order_item = OrderItem(
        params["order_id"],
        params["sku"],
        params["quantity"],
    )

    try:
        batch_reference = allocate(order_item, repository, session)

        return ({"reference": batch_reference}, 201)
    except (OutOfStock) as error:
        return ({"message": str(error)}, 400)
