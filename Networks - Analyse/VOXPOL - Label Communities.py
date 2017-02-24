###VOXPOL Network tools
#Auth: Jonathan Bright. Last update Feb 2017

#This file takes in output from the VOXPOL - Layout Communties script, in particular a user level dataset
#Such as "VOXPOL - Node Dataset - for visualisation.csv"
#this script automatically assigns labels to communities based on the text data contained within them
#this is useful when nodes have textual information attached to them

#insert infile name here
infile_name = "INPUT FILE1"






import csv
from nltk.corpus import stopwords
from nltk.stem.porter import *
import string
from collections import Counter



#remove punctuation, stopwords
#stem words
def proc(text):
    s = [c for c in text if c not in string.punctuation]
    text = "".join(s)
    stemmer = PorterStemmer()
    words = text.split(" ")
    filtered = [w for w in words if not w in stopwords.words('english')]
    stemmed = []
    for item in filtered:
        stemmed.append(stemmer.stem(item))
    return stemmed

infile = open(infile_name, "r", encoding="latin-1")

#first get the clusters and their corpus
#as well as a total corpus
#assumes the node "name" has relevant text information in it

corpus = []#a list of stemmed words
clusters = {}

for line in csv.DictReader(infile, delimiter=","):
    #line["title"] = line["title"].decode("ascii", "ignore")

    if not line["community_id"] in clusters:
        clusters[line["community_id"]] = [] 

    clusters[line["community_id"]].extend(proc(line["name"]))

    corpus.extend(proc(line["name"]))

#now go from these lists to frequencies
#corp_count = Counter(corpus)
#clust_count = {clid: Counter(clusters[clid]) for clid in clusters}


#%%
import nltk
from nltk.stem.porter import PorterStemmer
stemmer = PorterStemmer()
def stem_tokens(tokens, stemmer):
    stemmed = []
    for item in tokens:
        stemmed.append(stemmer.stem(item))
    return stemmed

def tokenize(text):
    tokens = nltk.word_tokenize(text)
    stems = stem_tokens(tokens, stemmer)
    return stems
    
    
from sklearn.feature_extraction.text import TfidfVectorizer
token_dict = {}
for cluster in clusters:
    text = " ".join(clusters[cluster])
    token_dict[cluster] = text
        
#this can take some time
tfidf = TfidfVectorizer(tokenizer=tokenize, stop_words='english')
tfs = tfidf.fit_transform(token_dict.values())


#%%
import pandas as pd

main_frame = pd.DataFrame(columns=["term", "tfidf", "clid"])

for tid in token_dict:

    s = token_dict[tid]
    response = tfidf.transform([s])
    
    d = []
    feature_names = tfidf.get_feature_names()
    for col in response.nonzero()[1]:
        d.append({"term":feature_names[col], "tfidf": response[0, col]})
        
    df = pd.DataFrame(d)
    df = df.sort_values("tfidf", ascending=False)
    top = df.head(10)
    top["clid"] = tid
    
    main_frame = main_frame.append(top)

mf = main_frame.groupby("clid").head(5)#top 5 terms: change number if you want more

clidterms = {}
for row in mf.iterrows():
    if not row[1]["clid"] in clidterms:
        clidterms[row[1]["clid"]]=row[1]["term"]
    else:
        clidterms[row[1]["clid"]]+=";"
        clidterms[row[1]["clid"]]+=row[1]["term"]
d=[]      
for clid in clidterms:
    d.append({"clid":clid, "term":clidterms[clid]})        
#%%
clid_df = pd.DataFrame(d)
        
clid_df.to_csv("VOXPOL - Cluster Names.csv")



