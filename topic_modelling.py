from bertopic import BERTopic
from umap import UMAP
from sklearn.feature_extraction.text import CountVectorizer

vectorizer_model = CountVectorizer(stop_words="english", max_df=0.7)
umap_model = UMAP(n_neighbors = 25)
topic_model = BERTopic(
                        umap_model = umap_model,
                        vectorizer_model = vectorizer_model,
                        verbose = True,
                        nr_topics = 25
                        )

conferences = ["acsac", "ccs", "dsn", "esorics", "raid", "sp", "uss"]
years = ["2012", "2013", "2014", "2015", "2016", "2017", "2018", "2019", "2020", "2021", "2022"]
docs = []

for conference in conferences:
    for year in years:
        with open(f"./{conference}/{conference}{year}.txt") as f:
            doc = f.read().splitlines()
            docs.extend(doc)

for doc in docs:
    if "www.w3.org/" in doc:
        docs.remove(doc)
    if doc == "":
        docs.remove(doc)

print("...")
print(docs[len(docs) - 1])

topics, probs = topic_model.fit_transform(docs)

print(topic_model.get_topic_info())