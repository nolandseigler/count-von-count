import os

from fastapi import Request

from count_von_count.counter import Counter, get_global_spacy


def get_nlp(request: Request) -> None:
    request.nlp = get_global_spacy()

def get_new_test_counter(request: Request) -> None:
    request.counter = Counter(
        nlp=get_global_spacy(),
        pdf_file_obj=os.environ["TEST_FILE"],
    )