import pickle

from pathlib import Path

import spacy

from tqdm import tqdm

from utils.articles import load_articles


def main():
    fr = spacy.load('fr_core_news_sm')

    df = load_articles()
    df["Mois"] = df['Date'].dt.to_period('M')
    df["Année"] = df['Date'].dt.to_period('Y')
    df["Publications"] = 1

    df["docs"] = list(tqdm(fr.pipe(df["full_text"].str.strip(), batch_size=32), total=len(df), desc="textes"))
    df["nb_tokens"] = df["docs"].apply(len)
    df["title_doc"] = list(tqdm(fr.pipe(df["Titre"].str.strip()), total=len(df), desc="titres"))

    with open(Path(__file__).parent / "canebiere.pickle", "wb") as out:
        pickle.dump(df, out)


if __name__ == "__main__":
    main()
