"""Allocate Service"""
from model import OrderItem
from model import allocate as allocate_item
from repository import AbstractStockBatchRepositoryPort


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

    batch_reference = allocate_item(item, batches)

    session.commit()

    return batch_reference
