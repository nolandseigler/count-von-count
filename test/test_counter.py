
import pytest
from count_von_count.counter import Counter


TEST_FILE = "/Users/nolandseigler/CodeProjects/count-von-count/data/fy25_air_force_working_capital_fund.pdf"

@pytest.mark.timeout(20)
@pytest.mark.limit_memory("120 MB")
def test_process():
    counter = Counter(
        pdf_filepath=TEST_FILE,
        page_batch_size=5
    )
    results = counter.process()
    assert results == {'largest': {'num': 9600000000.0, 'lemma': '$ 9.6 billion'}, 'no_context_largest': {'num': 6000000.0, 'lemma': '6,000,000'}}
