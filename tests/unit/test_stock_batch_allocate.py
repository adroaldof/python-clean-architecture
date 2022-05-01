"""Test allocation in batches"""
from datetime import date, timedelta

import pytest
from test_mocks import mock_order_id, mock_reference, mock_sku

from allocation.domain.order_item import OrderItem
from allocation.domain.out_of_stock_exception import OutOfStock
from allocation.domain.stock_batch import StockBatch, allocate

today = date.today()
tomorrow = today + timedelta(days=1)
later = tomorrow + timedelta(days=10)


def test_prefers_current_stock_batches_to_shipments():
    mocked_sku = mock_sku()

    in_stock_batch = StockBatch(mock_reference(), mocked_sku, 100, None)
    shipment_batch = StockBatch(mock_reference(), mocked_sku, 100, today)

    order_item = OrderItem(mock_order_id(), mocked_sku, 10)

    allocate(order_item, [in_stock_batch, shipment_batch])

    assert in_stock_batch.available_quantity == 90
    assert shipment_batch.available_quantity == 100


def test_prefer_earlier_batches():
    mocked_sku = mock_sku()

    today_batch = StockBatch(mock_reference(), mocked_sku, 100, today)
    tomorrow_batch = StockBatch(mock_reference(), mocked_sku, 100, tomorrow)
    later_batch = StockBatch(mock_reference(), mocked_sku, 100, later)

    order_item = OrderItem(mock_order_id(), mocked_sku, 10)

    allocate(order_item, [later_batch, today_batch, tomorrow_batch])

    assert today_batch.available_quantity == 90
    assert tomorrow_batch.available_quantity == 100
    assert later_batch.available_quantity == 100


def test_returns_allocated_batch_reference_on_allocate_line():
    mocked_sku = mock_sku()

    in_stock_batch = StockBatch(mock_reference(), mocked_sku, 100, None)
    shipment_batch = StockBatch(mock_reference(), mocked_sku, 100, today)

    order_item = OrderItem(mock_order_id(), mocked_sku, 10)

    allocated_batch_reference = allocate(order_item, [in_stock_batch, shipment_batch])

    assert allocated_batch_reference == in_stock_batch.reference


def test_raises_out_of_stock_exception_if_cannot_allocate():
    mocked_sku = mock_sku()

    batch = StockBatch(mock_reference(), mocked_sku, 22, today)

    order_item = OrderItem(mock_order_id(), mocked_sku, 33)

    with pytest.raises(OutOfStock, match=mocked_sku):
        allocate(order_item, [batch])
