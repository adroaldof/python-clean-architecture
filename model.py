from datetime import date
from dataclasses import dataclass
from typing import Optional


@dataclass(frozen=True)
class OrderLine:
    order_id: str
    sku: str
    quantity: int


class Batch:
    def __init__(
        self, reference: str, sku: str, quantity: int, purchase_date: Optional[date]
    ) -> None:
        self.reference = reference
        self.sku = sku
        self.purchase_date = purchase_date
        self.available_quantity = quantity

    def allocate(self, line: OrderLine):
        self.available_quantity -= line.quantity
