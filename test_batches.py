from datetime import date
from model import Batch, OrderLine

from test_faker import fake, mock_sentence, mock_uuid


def make_batch_and_line(sku: str, batch_quantity: int, line_quantity: int):
    batch_name = mock_sentence()

    return (
        Batch(batch_name, sku, quantity=batch_quantity, purchase_date=date.today()),
        OrderLine(fake.unique.first_name(), sku, line_quantity),
    )


def test_allocating_to_a_batch_reduces_the_available_quantity():

    batch, line = make_batch_and_line(mock_uuid(), 20, 2)

    batch.allocate(line)

    assert batch.available_quantity == 18
