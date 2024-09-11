import os

from fastapi import Request

from count_von_count.counter import Counter



def get_new_test_counter(request: Request) -> None:
    request.counter = Counter(
        pdf_filepath=os.environ["TEST_FILE"],
        page_batch_size=5
    )