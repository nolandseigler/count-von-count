
import time
from count_von_count.counter import Counter


def main():

    counter = Counter(
        pdf_filepath="/Users/nolandseigler/CodeProjects/count-von-count/data/fy25_air_force_working_capital_fund.pdf",
        page_batch_size=5
    )
    start = time.time()
    results = counter.process()
    end = time.time()
    print(f"executed in {end - start} seconds, {counter._page_batch_size=}, {counter._num_processing_proc=}  {results=}")





if __name__ == "__main__":
    main()
