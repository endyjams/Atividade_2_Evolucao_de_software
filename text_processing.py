"""
text_processing.py

Este módulo realiza o pré-processamento dos textos das issues, incluindo:
- Limpeza dos textos (remoção de URLs, caracteres especiais, stopwords).
- Modelagem de tópicos com TF-IDF e LDA.
- Extração de palavras-chave relacionadas a discussões de valor e gerência de mudanças.
"""

import re
import nltk
from nltk.corpus import stopwords
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.decomposition import LatentDirichletAllocation

# Baixa as stopwords se necessário
nltk.download('stopwords')

def preprocess_text(text):
    """
    Limpa e normaliza o texto:
    - Remove URLs.
    - Remove caracteres especiais e números.
    - Converte para caixa baixa.
    - Remove stopwords (em português).
    """
    text = re.sub(r'http\S+', '', text)
    text = re.sub(r'[^a-zA-Z\s]', '', text)
    text = text.lower()
    tokens = text.split()
    stop_words = set(stopwords.words('portuguese'))
    tokens = [word for word in tokens if word not in stop_words]
    return " ".join(tokens)

def extract_issue_texts(issues):
    """
    Combina título e corpo de cada issue e aplica o pré-processamento.
    Retorna uma lista de textos processados.
    """
    texts = []
    for issue in issues:
        title = issue.get("title") or ""
        body = issue.get("body") or ""
        combined = title + " " + body
        processed = preprocess_text(combined)
        texts.append(processed)
    return texts

def perform_topic_modeling(texts, n_topics=5):
    """
    Realiza a vetorização com TF-IDF e aplica LDA para extrair tópicos.
    Retorna o modelo LDA, o vetor TF-IDF e o vectorizer.
    """
    vectorizer = TfidfVectorizer(max_df=0.95, min_df=2, stop_words='english')
    tfidf = vectorizer.fit_transform(texts)
    lda = LatentDirichletAllocation(n_components=n_topics, random_state=42)
    lda.fit(tfidf)
    return lda, vectorizer, tfidf

def display_topics(lda, feature_names, n_top_words=10):
    """
    Extrai os termos mais representativos para cada tópico.
    Retorna um dicionário com os tópicos e suas palavras-chave.
    """
    topics = {}
    for topic_idx, topic in enumerate(lda.components_):
        topics[topic_idx] = [feature_names[i] for i in topic.argsort()[:-n_top_words - 1:-1]]
    return topics

def count_keywords(texts, keywords):
    """
    Conta a ocorrência de cada palavra-chave nos textos.
    Retorna um dicionário com os termos e suas contagens.
    """
    counts = {kw: 0 for kw in keywords}
    for text in texts:
        for kw in keywords:
            if kw in text:
                counts[kw] += 1
    return counts
