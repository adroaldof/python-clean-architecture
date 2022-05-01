"""Test batches"""
from datetime import date

from test_mocks import mock_order_id, mock_sentence, mock_sku

from allocation.domain.order_item import OrderItem
from allocation.domain.stock_batch import StockBatch


def make_batch_and_line(sku: str, batch_quantity: int, line_quantity: int):
    batch_na = mock_sentence()

    return (
        StockBatch(batch_na, sku, quantity=batch_quantity, purchase_date=date.today()),
        OrderItem(mock_order_id(), sku, line_quantity),
    )


def test_allocating_to_a_batch_reduces_the_available_quantity():
    batch, line = make_batch_and_line(mock_sku(), 20, 3)

    batch.allocate(line)

    assert batch.available_quantity == 17


def test_ensures_allocation_is_idempotent():
    batch, line = make_batch_and_line(mock_sku(), 20, 3)

    batch.allocate(line)
    batch.allocate(line)

    assert batch.available_quantity == 17


def test_can_allocate_when_quantity_available_is_greather_than_required():
    batch, line = make_batch_and_line(mock_sku(), 20, 3)

    assert batch.can_allocate(line)


def test_cannot_allocate_when_quantity_available_is_lower_than_required():
    batch, line = make_batch_and_line(mock_sku(), 3, 20)

    assert batch.can_allocate(line) is False


def test_cannot_allocate_if_line_sku_do_not_match_bash_sku():
    batch_sku = mock_sku()
    line_sku = mock_sku()

    batch = StockBatch(mock_sentence(), batch_sku, 20, date.today())
    order_item = OrderItem(mock_order_id(), line_sku, 2)

    assert batch.can_allocate(order_item) is False


def test_can_only_deallocate_allocated_lines():
    batch, line = make_batch_and_line(mock_sku(), 20, 3)

    batch.deallocate(line)

    assert batch.available_quantity == 20
