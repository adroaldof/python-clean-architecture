"""Flask APP API"""
from typing import Any, Dict

from flask import Flask, request
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

from allocation.adapters import orm
from allocation.adapters.repository import StockBatchRepositoryAdapter
from allocation.config import get_postgres_uri
from allocation.domain.model import OrderItem, OutOfStock
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
    repository = StockBatchRepositoryAdapter(session)

    params: Dict[str, Any] = request.json  # type: ignore

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
