import pickle

from pathlib import Path

import numpy as np
import pandas as pd
import spacy

from tqdm import tqdm
tqdm.pandas()


def main():
    fr = spacy.load('fr_core_news_sm')

    df = pd.concat(pd.read_json(jsonl, orient="record", lines=True, convert_dates=False) for jsonl in Path("scraper").glob("*.jsonl"))

    df.columns = ["Titre", "Date", "Commentaires","html", "full_text", "url", "Auteur"]
    df["Date"] = pd.to_datetime(df["Date"], dayfirst=True)
    df["Mois"] = df['Date'].dt.to_period('M')
    df["Année"] = df['Date'].dt.to_period('Y')
    df["Publications"] = 1

    df["docs"] = df["full_text"].str.strip().progress_apply(fr)
    df["nb_tokens"] = df["docs"].apply(len)
    df["title_doc"] = df["Titre"].str.strip().progress_apply(fr)

    with open("canebiere.pickle", "wb") as out:
        pickle.dump(df, out)


if __name__ == "__main__":
    main()
