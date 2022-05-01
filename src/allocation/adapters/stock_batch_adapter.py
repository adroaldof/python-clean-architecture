"""Stock Batch Repository"""
from typing import Set

from allocation.adapters.stock_batch_port import StockBatchPort
from allocation.domain.stock_batch import StockBatch


class StockBatchAdapter(StockBatchPort):
    """Stock batch repository adapter"""

    def __init__(self, session):
        self.session = session

    def add(self, batch: StockBatch):
        self.session.add(batch)

    def get(self, reference: str) -> StockBatch:
        return self.session.query(StockBatch).filter_by(reference=reference).one()

    def list(self) -> Set[StockBatch]:
        return self.session.query(StockBatch).all()
