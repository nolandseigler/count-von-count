from pypdf import PdfReader

"""
Process each page and just save the highest number.

Some pages have headers that say things like "(Dollars in Millions)" and "(Dollars in Thousands)"
so for these pages factor that in.

The reality is that we know the document structure and there is likely some summary pages
that we should optimize for. this would prevent this program from being generalized so be careful.

"""

# python -m spacy download en_core_web_sm
import spacy

def main():
    nlp = spacy.load("en_core_web_sm")
    # Merge noun phrases and entities for easier analysis
    nlp.add_pipe("merge_entities")
    nlp.add_pipe("merge_noun_chunks")

    reader = PdfReader("/Users/nolandseigler/CodeProjects/count-von-count/data/fy25_air_force_working_capital_fund.pdf")
    for page in reader.pages:
        # TODO: better with or without newlines?
        # def slower but might make processing easier?
        text = page.extract_text().replace("$ ", "$")
        # .replace("\n", "").replace("  ", " ")
        # TODO: another gross O(n^2) thing that is prob not great
        in_millions_page = "(Dollars in Millions)" in text and "Budget Estimates" in text
        in_thousands_page = "(Dollars in Thousands)" in text and "Budget Estimates" in text
        in_millions_summary_page = "AFWCF Financial Summary" in text and "(Dollars in Millions)" in text
        # TODO: prob something that can be done to optimize this
        # https://spacy.io/usage/linguistic-features#section-dependency-parse:~:text=The%20dependency%20parse,9.4%20million%22.
        if "billion" in text:
            pass
        for doc in nlp.pipe(texts=[text]):
            for token in doc:
                if "billion" in token.lemma_:
                    pass
                # nlp.meta["labels"]["ner"]
                # ['CARDINAL', 'DATE', 'EVENT', 'FAC', 'GPE', 'LANGUAGE', 'LAW', 'LOC', 'MONEY', 'NORP', 'ORDINAL', 'ORG', 'PERCENT', 'PERSON', 'PRODUCT', 'QUANTITY', 'TIME', 'WORK_OF_ART']

                # any other way to get a list of all ent_type_ ??

                # here is from smashing them all in this doc into a sec: {'', 'ORDINAL', 'EVENT', 'DATE', 'NORP', 'PERSON', 'GPE', 'WORK_OF_ART', 'PERCENT', 'LAW', 'QUANTITY', 'PRODUCT', 'MONEY', 'CARDINAL', 'FAC', 'ORG', 'TIME', 'LOC'}
                if token.ent_type_ == "MONEY":
                    splitty = token.lemma_.split(" ")
                    # .replace("\n", "").replace("  ", " ")
                    # ['1']
                    if len(splitty) != 2:
                        continue
                    # ['$1,088.6', 'million']
                    if splitty[1] == "million":
                        continue
                    if splitty[1] == "thousand":
                        continue
                    if splitty[1] == "billion":
                        continue
                    # some of these will have a length of 2 and maybe one
                    # and they will be like page 16 where we can pull the table header
                    # ($ Millions) FY 2023 FY 2024 FY 2025
                    # to calculate or unit
                    pass
                # theres something to be had here but it might not be worth the effort at the moment.
                # this seems to hit on the tables the most
                # example outputs
                # 0.000000 179.76 0.000
                # .012 .742 .693
                elif token.ent_type_ == "QUANTITY":
                    pass
        if "billion" in text:
            pass



if __name__ == "__main__":
    main()
