"""Object Relational Mapper"""
from sqlalchemy import Column, Date, ForeignKey, Integer, MetaData, String, Table
from sqlalchemy.orm import mapper, relationship

import model

metadata = MetaData()

order_items = Table(
    "order_item",
    metadata,
    Column("id", Integer, primary_key=True, autoincrement=True),
    Column("order_id", String(255)),
    Column("sku", String(255)),
    Column("quantity", Integer, nullable=False),
)

stock_batches = Table(
    "stock_batch",
    metadata,
    Column("id", Integer, primary_key=True, autoincrement=True),
    Column("reference", String(255)),
    Column("sku", String(255)),
    Column("purchase_date", Date, nullable=True),
    Column("_purchased_quantity", Integer, nullable=False),
)

allocations = Table(
    "allocation",
    metadata,
    Column("id", Integer, primary_key=True, autoincrement=True),
    Column("order_item_id", ForeignKey("order_item.id")),
    Column("batch_id", ForeignKey("stock_batch.id")),
)


def start_mappers():
    order_items_mapper = mapper(model.OrderItem, order_items)

    mapper(
        model.StockBatch,
        stock_batches,
        properties={
            "_allocations": relationship(
                order_items_mapper,
                secondary=allocations,
                collection_class=set,
            )
        },
    )
