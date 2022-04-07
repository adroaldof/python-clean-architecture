from datetime import date
from dataclasses import dataclass
from typing import List, Optional


class OutOfStock(Exception):
    pass


@dataclass(frozen=True)
class OrderItem:
    order_id: str
    sku: str
    quantity: int


class StockBatch:
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
        self._allocations = set()

    def allocate(self, line: OrderItem):
        if self.can_allocate(line):
            self._allocations.add(line)

    def deallocate(self, line: OrderItem):
        if line in self._allocations:
            self._allocations.remove(line)

    @property
    def allocated_quantity(self) -> int:
        return sum(line.quantity for line in self._allocations)

    @property
    def available_quantity(self) -> int:
        return self._purchased_quantity - self.allocated_quantity

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


def allocate(line: OrderItem, batches: List[StockBatch]) -> str:
    try:
        selected_batch = next(
            batch for batch in sorted(batches) if batch.can_allocate(line)
        )

        selected_batch.allocate(line)

        return selected_batch.reference
    except StopIteration:
        raise OutOfStock(f"Out of stock sku {line.sku}")
