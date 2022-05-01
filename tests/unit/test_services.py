"""Test allocation services"""
import pytest
from test_mocks import mock_order_id, mock_reference, mock_sku

from allocation.adapters.stock_batch_port import StockBatchPort
from allocation.domain.order_item import OrderItem
from allocation.domain.stock_batch import StockBatch
from allocation.service.services import InvalidSku, allocate


class FakeRepository(StockBatchPort):
    """
    Fake repository to be used in the allocation services tests. It uses the
    stock batch port to ensure the to test only the service and leave the
    repository to have its own tests
    """

    def __init__(self, batches):
        self._batches = set(batches)

    def add(self, batch):
        self._batches.add(batch)

    def get(self, reference):
        return next(b for b in self._batches if b.reference == reference)

    def list(self):
        return list(self._batches)


class FakeSession:  # pylint: disable=too-few-public-methods
    """Fake session to be used in the allocation services tests"""

    def __init__(self):
        self.commited = False

    def commit(self):
        self.commited = True


def test_return_allocation():
    mocked_sku = mock_sku()
    mocked_reference = mock_reference()

    order_item = OrderItem(mock_order_id(), mocked_sku, 10)
    batch = StockBatch(mocked_reference, mocked_sku, 100, None)
    repository = FakeRepository([batch])

    result = allocate(order_item, repository, FakeSession())

    assert result == mocked_reference


def test_raise_error_when_passing_invalid_sku():
    invalid_mocked_sku = mock_sku()
    mocked_reference = mock_reference()

    order_item = OrderItem(mock_order_id(), invalid_mocked_sku, 10)
    batch = StockBatch(mocked_reference, mock_sku(), 100, None)
    repository = FakeRepository([batch])

    with pytest.raises(InvalidSku, match=f"Invalid SKU {invalid_mocked_sku}"):
        allocate(order_item, repository, FakeSession())


def test_session_commits():
    mocked_sku = mock_sku()

    order_item = OrderItem(mock_order_id(), mocked_sku, 10)
    batch = StockBatch(mock_reference(), mocked_sku, 100, None)
    repository = FakeRepository([batch])
    session = FakeSession()

    allocate(order_item, repository, session)
    assert session.commited is True
