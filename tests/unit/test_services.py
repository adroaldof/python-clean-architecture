"""Test allocation services"""
import pytest
from test_mocks import mock_order_id, mock_reference, mock_sku

from allocation.adapters.repository import AbstractStockBatchRepositoryPort
from allocation.domain.model import OrderItem, StockBatch
from allocation.service.services import InvalidSku, allocate


class FakeRepository(AbstractStockBatchRepositoryPort):
    """Fake repository to be used in the allocation services tests"""

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

    item = OrderItem(mock_order_id(), mocked_sku, 10)
    batch = StockBatch(mocked_reference, mocked_sku, 100, None)
    repository = FakeRepository([batch])

    result = allocate(item, repository, FakeSession())

    assert result == mocked_reference


def test_raise_error_when_passing_invalid_sku():
    invalid_mocked_sku = mock_sku()
    mocked_reference = mock_reference()

    item = OrderItem(mock_order_id(), invalid_mocked_sku, 10)
    batch = StockBatch(mocked_reference, mock_sku(), 100, None)
    repository = FakeRepository([batch])

    with pytest.raises(InvalidSku, match=f"Invalid SKU {invalid_mocked_sku}"):
        allocate(item, repository, FakeSession())


def test_session_commits():
    mocked_sku = mock_sku()

    item = OrderItem(mock_order_id(), mocked_sku, 10)
    batch = StockBatch(mock_reference(), mocked_sku, 100, None)
    repository = FakeRepository([batch])
    session = FakeSession()

    allocate(item, repository, session)
    assert session.commited is True
