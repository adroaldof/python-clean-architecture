"""Module to provide StockBatch model"""
from dataclasses import dataclass
from datetime import date
from typing import List, Optional, Set


class OutOfStock(Exception):
    """Out of stock exception"""


@dataclass(unsafe_hash=True)
class OrderItem:
    """Order item data class that represents a new value in the stock"""

    order_id: str
    sku: str
    quantity: int


class StockBatch:
    """Holds all batches from the current stock"""

    def __init__(
        self,
        reference: str,
        sku: str,
        quantity: int,
        purchase_date: Optional[date],
    ) -> None:
        self.reference = reference
        self.sku = sku
        self.purchase_date = purchase_date
        self._purchased_quantity = quantity
        self._allocations: Set[OrderItem] = set()

    @property
    def allocated_quantity(self) -> int:
        return sum(line.quantity for line in self._allocations)

    @property
    def available_quantity(self) -> int:
        return self._purchased_quantity - self.allocated_quantity

    def allocate(self, line: OrderItem):
        if self.can_allocate(line):
            self._allocations.add(line)

    def deallocate(self, line: OrderItem):
        if line in self._allocations:
            self._allocations.remove(line)

    def can_allocate(self, line: OrderItem) -> bool:
        return self.sku == line.sku and self._purchased_quantity >= line.quantity

    def __eq__(self, compared_instance) -> bool:
        if not isinstance(compared_instance, StockBatch):
            return False

        return compared_instance.reference == self.reference

    def __hash__(self) -> int:
        return hash(self.reference)

    def __gt__(self, compared_entity):
        if self.purchase_date is None:
            return False

        if compared_entity.purchase_date is None:
            return True

        return self.purchase_date > compared_entity.purchase_date


def allocate(item: OrderItem, batches: List[StockBatch]) -> str:
    try:
        selected_batch = next(
            batch for batch in sorted(batches) if batch.can_allocate(item)
        )

        selected_batch.allocate(item)

        return selected_batch.reference
    except StopIteration as raised_exception:
        raise OutOfStock(f"Out of stock sku {item.sku}") from raised_exception
