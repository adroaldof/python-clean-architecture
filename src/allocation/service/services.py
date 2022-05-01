"""Allocate Service"""
from allocation.adapters.repository import StockBatchPort
from allocation.domain.order_item import OrderItem
from allocation.domain.stock_batch import allocate as allocate_item


class InvalidSku(Exception):
    """Invalid SKU Exception"""


def is_valid_sku(sku, batches):
    return sku in {batch.sku for batch in batches}


def allocate(order_item: OrderItem, repository: StockBatchPort, session) -> str:
    batches = repository.list()

    if not is_valid_sku(order_item.sku, batches):
        raise InvalidSku(f"Invalid SKU {order_item.sku}")

    batch_reference = allocate_item(order_item, list(batches))

    session.commit()

    return batch_reference
