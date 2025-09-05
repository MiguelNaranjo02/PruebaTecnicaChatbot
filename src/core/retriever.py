from typing import List, Tuple, Optional
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import cosine_similarity
import numpy as np

class FAQRetriever:
    def __init__(self, faqs: List[dict], ngram_range=(1,2), max_features=5000):
        self.questions = [f["question"] for f in faqs]
        self.answers = [f["answer"] for f in faqs]
        self.categories = [f.get("category", "información") for f in faqs]
        self.vectorizer = TfidfVectorizer(ngram_range=ngram_range, max_features=max_features)
        self.matrix = self.vectorizer.fit_transform(self.questions)

    def query(self, text: str, top_k: int = 3) -> List[Tuple[int, float]]:
        qv = self.vectorizer.transform([text])
        sims = cosine_similarity(qv, self.matrix)[0]
        idxs = np.argsort(-sims)[:top_k]
        return [(int(i), float(sims[i])) for i in idxs]

    def best_match(self, text: str) -> Tuple[Optional[str], Optional[str], float]:
        results = self.query(text, top_k=1)
        if not results:
            return None, None, 0.0
        i, score = results[0]
        return self.answers[i], self.categories[i], score