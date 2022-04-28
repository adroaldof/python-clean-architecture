"""Mock helper functions"""
from faker import Faker

fake = Faker()


def mock_reference() -> str:
    return f"ref-{fake.uuid4()}"


def mock_sku() -> str:
    return f"sku-{fake.ean13()}"


def mock_order_id() -> str:
    return f"order-{fake.uuid4()}"


def mock_sentence(number_of_words: int = 2) -> str:
    return fake.sentence(number_of_words)
