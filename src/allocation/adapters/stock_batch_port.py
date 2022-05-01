"""Stock Batch Repository"""
import abc
from typing import Set

from allocation.domain.stock_batch import StockBatch


class StockBatchPort(abc.ABC):
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
