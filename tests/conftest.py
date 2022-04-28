"""Memory Database Test configuration"""
import time
from pathlib import Path

import pytest
import requests
from sqlalchemy import create_engine
from sqlalchemy.exc import OperationalError
from sqlalchemy.orm import clear_mappers, sessionmaker

from allocation.adapters.orm import metadata, start_mappers
from allocation.config import get_api_url, get_postgres_uri


@pytest.fixture
def in_memory_db():
    in_memory_db_engine = create_engine("sqlite:///:memory:")
    metadata.create_all(in_memory_db_engine)

    return in_memory_db_engine


@pytest.fixture
def session(in_memory_db):  # pylint: disable=redefined-outer-name
    start_mappers()
    yield sessionmaker(bind=in_memory_db)()
    clear_mappers()


def wait_for_postgres_to_come_up(engine):
    timeout = time.time() + 10

    while time.time() < timeout:
        try:
            connection = engine.connect()

            return connection
        except OperationalError as error:
            print("OperationalError:", error)
            time.sleep(0.5)

    pytest.fail("Postgres couldn't be started")


def wait_for_webapp_to_come_up():
    timeout = time.time() + 10
    url = get_api_url()

    while time.time() < timeout:
        try:
            response = requests.get(url)

            return response
        except ConnectionError as error:
            print("ConnectionError:", error)
            time.sleep(0.5)

    pytest.fail("API couldn't be started")


@pytest.fixture(scope="session")
def postgres_db():
    database_url = get_postgres_uri()
    engine = create_engine(database_url)
    wait_for_postgres_to_come_up(engine)
    metadata.create_all(engine)

    return engine


@pytest.fixture
def postgres_session(postgres_db):  # pylint: disable=redefined-outer-name
    start_mappers()
    yield sessionmaker(bind=postgres_db)()
    clear_mappers()


@pytest.fixture
def restart_api():
    raw_app_path = Path(__file__).parent / "../src/allocation/entrypoint/flask_app.py"
    flask_app_path = Path(raw_app_path).resolve()
    (flask_app_path).touch()
    time.sleep(0.5)
    wait_for_webapp_to_come_up()


@pytest.fixture
def add_stock(postgres_session):  # pylint: disable=redefined-outer-name
    batches_added = set()
    skus_added = set()

    def _add_stock(lines):
        for reference, sku, quantity, purchase_date in lines:
            postgres_session.execute(
                "insert into stock_batch (reference, sku, _purchased_quantity, purchase_date)"
                " values (:reference, :sku, :quantity, :purchase_date)",
                dict(
                    reference=reference,
                    sku=sku,
                    quantity=quantity,
                    purchase_date=purchase_date,
                ),
            )
            [[batch_id]] = postgres_session.execute(
                "select id from stock_batch where reference=:reference AND sku=:sku",
                dict(reference=reference, sku=sku),
            )

            batches_added.add(batch_id)
            skus_added.add(sku)

        postgres_session.commit()

    yield _add_stock

    for batch_id in batches_added:
        postgres_session.execute(
            "delete from allocation where batch_id=:batch_id",
            dict(batch_id=batch_id),
        )
        postgres_session.execute(
            "delete from stock_batch where id=:batch_id",
            dict(batch_id=batch_id),
        )

    for sku in skus_added:
        postgres_session.execute(
            "delete from order_item where sku=:sku",
            dict(sku=sku),
        )
        postgres_session.commit()
