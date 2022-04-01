from datetime import date
from model import Batch, OrderLine
from faker import Faker

fake = Faker()


def test_allocating_to_a_batch_reduces_the_available_quantity():
    product_name = fake.name()

    batch = Batch(fake.name(), product_name, quantity=20, purchase_date=date.today())
    line = OrderLine(fake.unique.first_name(), product_name, 2)

    batch.allocate(line)

    assert batch.available_quantity == 18
