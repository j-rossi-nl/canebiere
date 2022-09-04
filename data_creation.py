import pickle
import sys

from operator import xor
from pathlib import Path
from argparse import ArgumentParser

import numpy as np
import pandas as pd
import spacy

from tqdm import tqdm
tqdm.pandas()


def main():
    parser = ArgumentParser('data-creation')
    group = parser.add_mutually_exclusive_group()
    group.add_argument('--all', action='store_true')
    group.add_argument('--last', action='store_true')

    args = parser.parse_args(sys.argv[1:])

    fr = spacy.load('fr_core_news_sm')

    if args.all:
        df = pd.concat(pd.read_json(jsonl, orient="record", lines=True) for jsonl in Path("scraper").glob("*.jsonl"))

        df.columns = ["Titre", "Date", "html", "full_text", "url", "Auteur"]
        df["Mois"] = df['Date'].dt.to_period('M')
        df["Année"] = df['Date'].dt.to_period('Y')
        df["Publications"] = 1

        df["docs"] = df["full_text"].str.strip().progress_apply(fr)
        df["nb_tokens"] = df["docs"].apply(len)
        df["title_doc"] = df["Titre"].str.strip().progress_apply(fr)

        with open("canebiere.pickle", "wb") as out:
            pickle.dump(df, out)

    if args.last:
        with open("canebiere.pickle", "rb") as src:
            df_all = pickle.load(src)

        jsons = Path("scraper").glob("*.jsonl")
        most_recent = sorted(jsons, key=lambda x: x.stat().st_mtime, reverse=True)[0]
        df = pd.read_json(most_recent, orient="record", lines=True, convert_dates=False) 

        df.columns = ["Titre", "Date", "Commentaires","html", "full_text", "url", "Auteur"]
        df["Date"] = pd.to_datetime(df["Date"], dayfirst=True)
        df["Mois"] = df['Date'].dt.to_period('M')
        df["Année"] = df['Date'].dt.to_period('Y')
        df["Publications"] = 1

        df["docs"] = df["full_text"].str.strip().progress_apply(fr)
        df["nb_tokens"] = df["docs"].apply(len)
        df["title_doc"] = df["Titre"].str.strip().progress_apply(fr)

        with open("canebiere.pickle", "wb") as out:
            pickle.dump(pd.concat([df_all, df]), out)
        

if __name__ == "__main__":
    main()
