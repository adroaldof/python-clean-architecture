import pytest
from datetime import date, timedelta
from model import Batch, OrderItem, allocate, OutOfStock
from test_mocks import mock_id, mock_refence, mock_sku

today = date.today()
tomorrow = today + timedelta(days=1)
later = tomorrow + timedelta(days=10)


def test_prefers_current_stock_batches_to_shipments():
    mocked_sku = mock_sku()

    in_stock_batch = Batch(mock_refence(), mocked_sku, 100, None)
    shipment_batch = Batch(mock_refence(), mocked_sku, 100, date.today())

    line = OrderItem(mock_id(), mocked_sku, 10)

    allocate(line, [in_stock_batch, shipment_batch])

    assert in_stock_batch.available_quantity == 90
    assert shipment_batch.available_quantity == 100


def test_prefer_earlier_batches():
    mocked_sku = mock_sku()

    today_batch = Batch(mock_refence(), mocked_sku, 100, today)
    tomorrow_batch = Batch(mock_refence(), mocked_sku, 100, tomorrow)
    later_batch = Batch(mock_refence(), mocked_sku, 100, later)

    line = OrderItem(mock_id(), mocked_sku, 10)

    allocate(line, [later_batch, today_batch, tomorrow_batch])

    assert today_batch.available_quantity == 90
    assert tomorrow_batch.available_quantity == 100
    assert later_batch.available_quantity == 100


def test_returns_allocated_batch_reference_on_allocate_line():
    mocked_sku = mock_sku()

    in_stock_batch = Batch(mock_refence(), mocked_sku, 100, None)
    shipment_batch = Batch(mock_refence(), mocked_sku, 100, today)

    line = OrderItem(mock_id(), mocked_sku, 10)

    allocated_batch_reference = allocate(line, [in_stock_batch, shipment_batch])

    assert allocated_batch_reference == in_stock_batch.reference


def test_raises_out_of_stock_exception_if_cannot_allocate():
    mocked_sku = mock_sku()

    batch = Batch(mock_refence(), mocked_sku, 22, today)

    line = OrderItem(mock_id(), mocked_sku, 33)

    with pytest.raises(OutOfStock, match=mocked_sku):
        allocate(line, [batch])
