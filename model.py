from datetime import date
from dataclasses import dataclass
from typing import NewType, Optional

OrderReference = NewType("OrderReference", str)
OrderId = NewType("OrderId", str)
SKU = NewType("SKU", str)


@dataclass(frozen=True)
class OrderItem:
    order_id: OrderId
    sku: SKU
    quantity: int


class Batch:
    def __init__(
        self,
        reference: OrderReference,
        sku: SKU,
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
