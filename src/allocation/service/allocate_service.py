"""Allocate Service"""
from allocation.adapters.stock_batch_port import StockBatchPort
from allocation.domain.order_item import OrderItem
from allocation.domain.stock_batch import allocate as allocate_item
from allocation.service.invalid_sku_exception import InvalidSku


def is_valid_sku(sku, batches):
    return sku in {batch.sku for batch in batches}


def allocate(order_item: OrderItem, repository: StockBatchPort, session) -> str:
    batches = repository.list()

    if not is_valid_sku(order_item.sku, batches):
        raise InvalidSku(f"Invalid SKU {order_item.sku}")

    batch_reference = allocate_item(order_item, list(batches))

    session.commit()

    return batch_reference
