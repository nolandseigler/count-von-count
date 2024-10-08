import os

import pytest

from count_von_count.counter import Counter, get_global_spacy


@pytest.mark.timeout(20)
@pytest.mark.limit_memory("120 MB")
def test_process():
    counter = Counter(
        nlp=get_global_spacy(), pdf_file_obj=os.environ["TEST_FILE"], page_batch_size=5
    )
    results = counter.process()
    assert results == {
        "largest": {"num": 9600000000.0, "lemma": "$ 9.6 billion"},
        "no_context_largest": {"num": 6000000.0, "lemma": "6,000,000"},
    }
