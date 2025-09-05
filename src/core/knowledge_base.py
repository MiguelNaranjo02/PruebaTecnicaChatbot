# src/core/knowledge_base.py
import os
import pandas as pd
from langchain_chroma import Chroma
from langchain_huggingface import HuggingFaceEmbeddings
from langchain.text_splitter import RecursiveCharacterTextSplitter



class KnowledgeBase:
    def __init__(self, embedding_model: str = "sentence-transformers/all-MiniLM-L6-v2", persist_directory: str = None):
        self.embeddings = HuggingFaceEmbeddings(model_name=embedding_model)

        # Si quieres persistir en disco, pasa un persist_directory (ej: "./chroma_db")
        self.vectorstore = Chroma(
            collection_name="faq",
            embedding_function=self.embeddings,
            persist_directory=persist_directory
        )

    def add_document(self, text: str):
        """Agrega un documento de texto a la base de conocimiento"""
        self.vectorstore.add_texts([text])

    def load_csv(self, path: str, question_col="question", answer_col="answer"):
        """Carga un CSV con preguntas y respuestas a la base de conocimiento"""
        if not os.path.exists(path):
            raise FileNotFoundError(f"El archivo {path} no existe.")

        df = pd.read_csv(path)
        for _, row in df.iterrows():
            q, a = row[question_col], row[answer_col]
            self.add_document(f"Q: {q}\nA: {a}")

        print(f"✅ {len(df)} pares cargados desde {path}")

    def load_markdown(self, file_path: str):
        """Carga un archivo markdown y lo indexa en Chroma"""
        if not os.path.exists(file_path):
            raise FileNotFoundError(f"El archivo {file_path} no existe.")

        with open(file_path, "r", encoding="utf-8") as f:
            text = f.read()

        splitter = RecursiveCharacterTextSplitter(chunk_size=500, chunk_overlap=50)
        docs = splitter.create_documents([text])

        self.vectorstore.add_documents(docs)
        print(f"✅ {len(docs)} fragmentos cargados desde {file_path}")

    def as_retriever(self):
        """Devuelve el retriever para usar en QA"""
        if not self.vectorstore:
            raise ValueError("Knowledge base vacía. Carga primero datos con load_csv() o load_markdown().")
        return self.vectorstore.as_retriever()
