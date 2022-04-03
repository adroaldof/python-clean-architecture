from faker import Faker

fake = Faker()


def mock_uuid() -> str:
    return fake.uuid4()


def mock_sentence(number_of_words: int = 2, variable_nb_words: bool = True) -> str:
    return fake.sentence(number_of_words, variable_nb_words)
