import requests
from bs4 import BeautifulSoup
import math
from collections import Counter


def LanguageModelling(query,urls):
    
    def MakeCorpus(URls):
        corpus = []
        for doc in URls:
            response = requests.get(doc)
            soup = BeautifulSoup(response.content, "html.parser")
            #print(doc,soup)
            #print(response)
            body = soup.find("body")
        if body is not None:
            content = body.get_text()
            corpus.append(content)
        return corpus


    corpus=MakeCorpus(urls)
    #language modeling This algorithm models the probability of a document being relevant to a query based on the likelihood of the query terms appearing in the document. The score is calculated using a statistical model of the language in both the query and the document.
    query_tokens = query.lower().split()
    corpus_tokens = [doc.lower().split() for doc in corpus]

    # Calculate document probabilities
    def DocumentProbabilites(corpus_tokens):
        doc_probs = []
        for doc in corpus_tokens:
            doc_count = Counter(doc)
            doc_length = len(doc)
            doc_prob = {}
            for term in query_tokens:
                term_freq = doc_count[term] if term in doc_count else 0
                try:
                    term_prob = (term_freq + 1) / (doc_length + len(set(doc)))
                except:
                    term_prob = (term_freq + 1) / (0.001)
                doc_prob[term] = term_prob
            doc_probs.append(doc_prob)
        return doc_probs

    # Calculate query probabilities
    def QuerProbability(query_tokens):
        query_count = Counter(query_tokens)
        query_length = len(query_tokens)
        query_probs = {}
        for term in query_tokens:
            term_freq = query_count[term] if term in query_count else 0
            term_prob = (term_freq + 1) / (query_length + len(set(query_tokens)))
            query_probs[term] = term_prob
        return query_probs

    # Calculate document scores
    doc_probs=DocumentProbabilites(corpus_tokens)
    query_probs=QuerProbability(query_tokens)
    def Scores(doc_probs,query_probs):
        doc_scores = []
        for i in range(len(corpus_tokens)):
            doc_score = 0
            for term in query_tokens:
                doc_score += math.log(doc_probs[i][term] * query_probs[term])
            doc_scores.append(doc_score)

        # Sort documents by score
        ranked_docs = [doc for _, doc in sorted(zip(doc_scores, urls), reverse=True)]

        d={}
        # Print ranked documents
        for i, doc in enumerate(ranked_docs):
            print(f"{i+1}. {doc}")
            d[doc]=i+1
        return d

    dic=Scores(doc_probs,query_probs)
    return dic