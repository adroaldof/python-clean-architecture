"""Test batch repository"""
from datetime import date

from model import StockBatch
from repository import StockBatchRepositoryAdapter
from test_mocks import mock_id, mock_reference, mock_sku


def insert_batch(
    session,
    reference: str = mock_reference(),
    sku: str = mock_sku(),
    quantity: int = 100,
    purchase_date: date = date.today(),
) -> str:
    batch_cursor = session.execute(
        "insert into"
        " stock_batch (reference, sku, _purchased_quantity, purchase_date)"
        " values (:reference, :sku, :quantity, :purchase_date)"
        " returning reference",
        dict(
            reference=reference, sku=sku, quantity=quantity, purchase_date=purchase_date
        ),
    )

    created_batch = batch_cursor.mappings().first()

    return created_batch.reference


def insert_order_item(
    session, order_id: str = mock_id(), sku: str = mock_sku(), quantity: int = 10
) -> str:
    session.execute(
        "insert into order_item (order_id, sku, quantity) values (:order_id, :sku, :quantity)",
        dict(order_id=order_id, sku=sku, quantity=quantity),
    )

    order_item_cursor = session.execute("select * from order_item")

    created_order_item = order_item_cursor.mappings().first()

    return created_order_item.id


def insert_allocation(session, batch_id: str, order_item_id: str):
    session.execute(
        "insert into allocation (order_item_id, batch_id) values (:order_item_id, :batch_id)",
        dict(order_item_id=order_item_id, batch_id=batch_id),
    )


def test_repository_can_save_a_batch(session):
    mocked_reference = mock_reference()
    mocked_sku = mock_sku()
    mocked_quantity = 100

    batch = StockBatch(mocked_reference, mocked_sku, mocked_quantity, None)

    repo = StockBatchRepositoryAdapter(session)
    repo.add(batch)
    session.commit()

    rows = list(
        session.execute(
            "select reference, sku, _purchased_quantity, purchase_date from stock_batch"
        )
    )

    assert rows == [(mocked_reference, mocked_sku, mocked_quantity, None)]


def test_repository_can_retrieve_a_batch_with_allocations(session):
    mocked_reference = mock_reference()
    mocked_sku = mock_sku()
    mocked_quantity = 100

    order_item_id = insert_order_item(session)
    batch_reference = insert_batch(
        session, mocked_reference, mocked_sku, mocked_quantity
    )

    insert_allocation(session, batch_reference, order_item_id)

    repo = StockBatchRepositoryAdapter(session)
    retrieved = repo.get(batch_reference)

    expected = StockBatch(mocked_reference, mocked_sku, mocked_quantity, None)
    assert retrieved == expected