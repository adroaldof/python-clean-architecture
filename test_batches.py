from datetime import date
from model import Batch, OrderLine
from faker import Faker

fake = Faker()


def make_batch_and_line(sku: str, batch_quantity: int, line_quantity: int):
    return (
        Batch(fake.name(), sku, quantity=batch_quantity, purchase_date=date.today()),
        OrderLine(fake.unique.first_name(), sku, line_quantity),
    )


def test_allocating_to_a_batch_reduces_the_available_quantity():
    sku = fake.name()

    batch, line = make_batch_and_line(sku, 20, 2)

    batch.allocate(line)

    assert batch.available_quantity == 18
