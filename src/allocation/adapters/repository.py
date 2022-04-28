"""Stock Batch Repository"""
import abc
from typing import Set

from allocation.domain.model import StockBatch


class AbstractStockBatchRepositoryPort(abc.ABC):
    """Stock batch repository port"""

    @abc.abstractmethod
    def add(self, batch: StockBatch):
        raise NotImplementedError

    @abc.abstractmethod
    def get(self, reference: str) -> StockBatch:
        raise NotImplementedError

    @abc.abstractmethod
    def list(self) -> Set[StockBatch]:
        raise NotImplementedError


class StockBatchRepositoryAdapter(AbstractStockBatchRepositoryPort):
    """Stock batch repository adapter"""

    def __init__(self, session):
        self.session = session

    def add(self, batch: StockBatch):
        self.session.add(batch)

    def get(self, reference: str) -> StockBatch:
        return self.session.query(StockBatch).filter_by(reference=reference).one()

    def list(self) -> Set[StockBatch]:
        return self.session.query(StockBatch).all()
