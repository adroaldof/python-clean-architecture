"""Allocate Service"""
from allocation.adapters.repository import AbstractStockBatchRepositoryPort
from allocation.domain.model import OrderItem
from allocation.domain.model import allocate as allocate_item


class InvalidSku(Exception):
    """Invalid SKU Exception"""


def is_valid_sku(sku, batches):
    return sku in {batch.sku for batch in batches}


def allocate(
    item: OrderItem, repository: AbstractStockBatchRepositoryPort, session
) -> str:
    batches = repository.list()

    if not is_valid_sku(item.sku, batches):
        raise InvalidSku(f"Invalid SKU {item.sku}")

    batch_reference = allocate_item(item, list(batches))

    session.commit()

    return batch_reference
