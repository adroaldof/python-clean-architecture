"""Mock helper functions"""
from faker import Faker

fake = Faker()


def mock_reference() -> str:
    return mock_id()


def mock_sku() -> str:
    return fake.ean13()


def mock_id() -> str:
    return fake.uuid4()


def mock_sentence(number_of_words: int = 2) -> str:
    return fake.sentence(number_of_words)
