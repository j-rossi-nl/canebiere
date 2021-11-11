import pandas as pd
import re

from wordcloud import WordCloud, STOPWORDS, ImageColorGenerator
from gensim.corpora import Dictionary
from gensim.models.ldamodel import LdaModel

# Load data
articles = pd.read_csv('canebiere.csv')
articles = articles.dropna()

all_tokens = [[w for w in re.sub("[^A-Za-z]", " ", t.lower()).split() if len(w)>3] for t in articles['text'].values]
dictionary = Dictionary(all_tokens)

# remove stopwords
from six import iteritems
from sklearn.feature_extraction.text import ENGLISH_STOP_WORDS

stoplist = set(ENGLISH_STOP_WORDS)

stop_ids = [dictionary.token2id[stopword] for stopword in stoplist if stopword in dictionary.token2id]
once_ids = [tokenid for tokenid, docfreq in iteritems(dictionary.dfs) if docfreq == 1]
dictionary.filter_tokens(stop_ids)  # remove stop words and words that appear only once
dictionary.compactify()  # remove gaps in id sequence after words that were removed

# counter corpus
counter = list(dictionary.doc2bow(text) for text in all_tokens)

num_topics = 5
lda = LdaModel(corpus=counter, id2word=dictionary, num_topics=num_topics)
topics = lda.show_topics(num_topics=num_topics, log=False, formatted=False)

print('Dictionary: {} docs, {} terms'.format(dictionary.num_docs, len(dictionary.dfs)))

for t in topics:
    t_str = "Topic {}: ".format(t[0])
    for w in t[1]:
        t_str += "{} ".format(w[0])
    print(t_str)

# The wordcloud
stoplist = set(ENGLISH_STOP_WORDS)
stoplist |= {"restaurant", "food", "place", "amsterdam"}
cloud = WordCloud(stopwords=stoplist, max_words=20, background_color='white').generate(' '.join([' '.join(x) for x in all_tokens]))
cloud.to_file('cloud.png')