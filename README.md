# count-von-count
Finds the largest number in a pdf document

## scratch

1. extract the text from the pdf using `insert lib here`
2. use some type of NER to get all numbers
3. find the biggest one.

cool poetry multistage build. looks legit.

https://github.com/gianfa/poetry/blob/docs/docker-best-practices/docker-examples/poetry-multistage/Dockerfile

tell users to download this file themselves: https://www.saffm.hq.af.mil/Portals/84/documents/FY25/FY25%20Air%20Force%20Working%20Capital%20Fund.pdf?ver=sHG_i4Lg0IGZBCHxgPY01g%3d%3d and put it at `data/fy25_air_force_working_capital_fund.pdf`. so we dont check this beast into git. it doesnt like VPN so turn that off if your download fails. thankss chairforce.

well this looks cool and quite convenient: https://github.com/DerwenAI/spaCy_tuTorial/blob/master/Extract_Text_from_PDF.ipynb

that ^^ use a python pdf lib that is only 3.9 and back. worst case we use that but this looks like the latest and greatest in python pdf: https://github.com/py-pdf/pypdf


mmmmmm spaaaccyyyy: https://spacy.io/usage/linguistic-features#section-dependency-parse:~:text=The%20dependency%20parse,9.4%20million%22.

