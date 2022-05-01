"""Order item data class"""
from dataclasses import dataclass


@dataclass(unsafe_hash=True)
class OrderItem:
    """Order item data class that represents a new product in the stock"""

    order_id: str
    sku: str
    quantity: int
