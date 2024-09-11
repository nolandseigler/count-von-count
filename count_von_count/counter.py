
"""
Process each page and just save the highest number.

Some pages have headers that say things like "(Dollars in Millions)" and "(Dollars in Thousands)"
so for these pages factor that in.

The reality is that we know the document structure and there is likely some summary pages
that we should optimize for. this would prevent this program from being generalized so be careful.

"""
from enum import StrEnum
import os
import re
from typing import Union
from pypdf import PdfReader
import spacy.tokens
# python -m spacy download en_core_web_sm
import spacy

class Multipliers(StrEnum):
    BILLION = "billion"
    MILLION = "million"
    THOUSAND = "thousand"


class Counter:

    BILLION = 1_000_000_000
    MILLION = 1_000_000
    THOUSAND = 1_000

    _nlp: spacy.language.Language
    _reader: PdfReader
    _num_processing_proc: int
    _garbage_filter: re.Pattern
    _page_batch_size: int

    _largest_num_token_lemma: str
    _largest_num: float

    _no_ctx_largest_num_token_lemma: str
    _no_ctx_largest_num: float

    __slots__ = (
       "_nlp",
       "_reader",
       "_num_processing_proc",
       "_garbage_filter",
       "_page_batch_size",
       "_largest_num_token_lemma",
       "_largest_num",
       "_no_ctx_largest_num_token_lemma",
       "_no_ctx_largest_num",
    )

    def __init__(self, pdf_filepath: str, page_batch_size: int = 10, num_processing_proc: int = 1) -> None:
        nlp = spacy.load("en_core_web_sm")
        # # Merge noun phrases and entities for easier analysis
        nlp.add_pipe("merge_entities")
        self._nlp = nlp
        self._reader = PdfReader(pdf_filepath)
        self._garbage_filter = re.compile(r"\b(?:\d{1,3}(?:,\d{3})*)\$")
        self._page_batch_size = page_batch_size

        self._num_processing_proc = num_processing_proc

        self._largest_num_token_lemma = ""
        self._largest_num = 0.0

        self._no_ctx_largest_num_token_lemma = ""
        self._no_ctx_largest_num = 0.0

    def _count_split_no_ctx(self, split: list[str], lemma: str):
        for x in split:
            x = x.replace("$", "").replace(",", "")
            if not x.isnumeric() and "." not in x:
                continue
            try:
                x = float(x)
            except ValueError:
                continue
            if x > self._no_ctx_largest_num:
                self._no_ctx_largest_num = x
                self._no_ctx_largest_num_token_lemma = lemma

    def _counts_split_len_2(self, split: list[str], lemma: str):
        # ['$1,088.6', 'million']
        num = split[0].replace("$", "").replace(",", "")
        if not num.isnumeric() and "." not in num:
            return
        try:
            num = float(num)
        except ValueError:
            return

        # ordered by most common first
        if split[1] == Multipliers.MILLION:
            val = num * self.MILLION
        elif split[1] == Multipliers.THOUSAND:
            val = num * self.THOUSAND
        elif split[1] == Multipliers.BILLION:
            val = num * self.BILLION
        else:
            return

        if val > self._largest_num:
            self._largest_num = val
            self._largest_num_token_lemma = lemma

    def _count_money_token(self, token: spacy.tokens.Token):
        if self._garbage_filter.match(token.lemma_) is not None:
            return

        splitty = token.lemma_.lower().replace("\n", "").replace("\r", "").replace("\t", "").replace("$ ", "$").strip().split(" ")

        self._count_split_no_ctx(split=splitty, lemma=token.lemma_)

        splitty_len = len(splitty)
        # just going to take the L on these for now
        if splitty_len != 2:
            return

        self._counts_split_len_2(split=splitty, lemma=token.lemma_)

    def _count_pages(self, pages: list[str]):
        for doc in self._nlp.pipe(texts=pages, n_process=self._num_processing_proc):
            for token in doc:
                if token.ent_type_ == "MONEY":
                    self._count_money_token(token=token)

                # theres something to be had here but it might not be worth the effort at the moment.
                # this seems to hit on the tables the most
                # example outputs
                # 0.000000 179.76 0.000
                # .012 .742 .693
                # TODO: take the L on these for now
                elif token.ent_type_ == "QUANTITY":
                    pass

    def process(self) -> dict[str, dict[str, Union[str, float]]]:
        # https://spacy.io/usage/processing-pipelines
        pages = []
        for page in self._reader.pages:
            pages.append(page.extract_text())
            # TODO: prob something that can be done to optimize this
            # https://spacy.io/usage/linguistic-features#section-dependency-parse:~:text=The%20dependency%20parse,9.4%20million%22.
            if len(pages) == self._page_batch_size:
                self._count_pages(pages=pages)
                pages.clear()

        if pages:
            self._count_pages(pages=pages)

        return {
            "largest": {
                "num": self._largest_num,
                "lemma": self._largest_num_token_lemma,
            },
            "no_context_largest": {
                "num": self._no_ctx_largest_num,
                "lemma": self._no_ctx_largest_num_token_lemma,
            }
        }

