#!/usr/bin/env python3
import csv
import sys
import html
import unicodedata
import re

# Codes réellement présents dans les CSS
VALID_CODES = {
    "au", "ca", "fr", "gb", "jp", "nw", "nz", "sw", "us"
}

# Mapping explicite pays → code CSS
COUNTRY_MAP = {
    "France": "fr",
    "Belgique": "xx",  # pas dans les CSS
    "Suisse": "xx",    # idem
    "Canada": "ca",
    "États-Unis": "us",
    "Etats-Unis": "us",
    "United States": "us",
    "USA": "us",
    "Royaume-Uni": "gb",
    "United Kingdom": "gb",
    "UK": "gb",
    "Japon": "jp",
    "Japan": "jp",
    "Norvège": "nw",
    "Norway": "nw",
    "Nouvelle-Zélande": "nz",
    "New Zealand": "nz",
    "Suède": "sw",
    "Sweden": "sw",
    "Australie": "au",
    "Australia": "au",
}


def country_to_code(country: str) -> str:
    country = country.strip()
    if not country:
        return "xx"

    if country in COUNTRY_MAP:
        code = COUNTRY_MAP[country]
        return code if code in VALID_CODES else "xx"

    # fallback : slug basique → tentative de 2 lettres
    s = unicodedata.normalize("NFKD", country)
    s = "".join(c for c in s if not unicodedata.combining(c))
    s = re.sub(r"[^a-zA-Z]", " ", s).strip().lower()

    if not s:
        return "xx"
    first = s.split()[0]
    if len(first) < 2:
        first = (first + "x")[:2]
    code = first[:2]

    return code if code in VALID_CODES else "xx"


def main():
    rows = []

    with open("oped.tsv", encoding="utf-8") as f:
        reader = csv.reader(f, delimiter="\t")
        for cols in reader:
            if len(cols) < 3:
                continue

            fullname = cols[0].strip()
            lastname = cols[1].strip()
            desc = cols[2].strip()

            if "," in desc:
                body, country = desc.rsplit(",", 1)
                body = body.strip()
                country = country.strip()
            else:
                body, country = desc, ""

            code = country_to_code(country)

            # description visible (on garde le pays, comme dans l'exemple)
            if country:
                full_desc = f"{body}, {country}"
            else:
                full_desc = body

            rows.append((lastname, fullname, full_desc, code))

    rows.sort(key=lambda r: r[0].upper())

    out = sys.stdout
    for lastname, fullname, full_desc, code in rows:
        print('                            <tr>', file=out)
        print(f'                                <td><i class="country-{code}"> </i>', file=out)
        print(f'                                    {html.escape(fullname)}</td>', file=out)
        print(f'                                <td>{html.escape(full_desc)}</td>', file=out)
        print('                            </tr>', file=out)


if __name__ == "__main__":
    main()
