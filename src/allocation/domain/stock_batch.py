"""Module to provide StockBatch model"""
from datetime import date
from typing import List, Optional, Set

from allocation.domain.order_item import OrderItem
from allocation.domain.out_of_stock_exception import OutOfStock


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

    def allocate(self, order_item: OrderItem) -> None:
        if self.can_allocate(order_item):
            self._allocations.add(order_item)

    def deallocate(self, order_item: OrderItem) -> None:
        if order_item in self._allocations:
            self._allocations.remove(order_item)

    def can_allocate(self, order_item: OrderItem) -> bool:
        return (
            self.sku == order_item.sku
            and self._purchased_quantity >= order_item.quantity
        )

    def __eq__(self, compared_instance) -> bool:
        if not isinstance(compared_instance, StockBatch):
            return False

        return compared_instance.reference == self.reference

    def __hash__(self) -> int:
        return hash(self.reference)

    def __gt__(self, compared_entity) -> bool:
        if self.purchase_date is None:
            return False

        if compared_entity.purchase_date is None:
            return True

        return self.purchase_date > compared_entity.purchase_date


def allocate(order_item: OrderItem, batches: List[StockBatch]) -> str:
    try:
        selected_batch = next(
            batch for batch in sorted(batches) if batch.can_allocate(order_item)
        )

        selected_batch.allocate(order_item)

        return selected_batch.reference
    except StopIteration as raised_exception:
        raise OutOfStock(f"Out of stock SKU ({order_item.sku})") from raised_exception
