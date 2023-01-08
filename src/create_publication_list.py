from scholarly import scholarly
from dataclasses import dataclass
from typing import List


@dataclass
class bib_item:
    line: str
    type: str
    year: int


def create_bibliography(items: List[bib_item]):
    theses = [b for b in items if b.type == "thesis"]
    articles = [b for b in items if b.type == "article"]
    theses = sorted(theses, key=lambda x: x.year, reverse=True)
    articles = sorted(articles, key=lambda x: x.year, reverse=True)

    bib = (
        "## Theses\n\n"
        + "\n".join([t.line for t in theses])
        + "\n## Journal\n\n"
        + "\n".join([a.line for a in articles])
    )
    return bib


def bib_line(pub):
    if not pub["filled"]:
        scholarly.fill(pub)

    bib = pub["bib"]
    auths = str(bib["author"]).split(" and ")
    if len(auths) > 3:
        auth_line = f"{auths[0]} et al"
    elif len(auths) > 1:
        auth_line = ", ".join(auths[0:-1]) + f" and {auths[-1]}"
    else:
        auth_line = auths[0]

    line = f"{auth_line}. [*{bib['title']}*]({pub['pub_url']}). {bib['citation']}."

    if "Lethbridge" in bib["citation"] and len(auths) == 1:
        bib_type = "thesis"
    else:
        bib_type = "article"

    try:
        year = int(bib["pub_year"])
    except:
        year = 1

    return bib_item(line=line, type=bib_type, year=year)


me = next(scholarly.search_author("Ian Veenendaal"))
author = scholarly.fill(me)
pubs = author["publications"]
items = [bib_line(p) for p in pubs]

with open("bib.md", "w+") as f:
    c = create_bibliography(items)
    f.write(c)
