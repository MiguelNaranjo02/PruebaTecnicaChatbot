import requests

class Chatbot:
    def __init__(self, kb, retriever, config):
        self.kb = kb
        self.retriever = retriever
        self.config = config
        self.model = config["lm"]["model"]
        self.base_url = config["lm"]["base_url"]

    def query_llm(self, prompt: str) -> str:
        """Llamar a LM Studio usando API OpenAI compatible"""
        try:
            url = f"{self.base_url}/chat/completions"
            payload = {
                "model": self.model,
                "messages": [
                    {"role": "system", "content": "Eres un asistente útil y experto de la empresa."},
                    {"role": "user", "content": prompt}
                ]
            }
            r = requests.post(url, json=payload)
            r.raise_for_status()
            data = r.json()
            return data["choices"][0]["message"]["content"].strip()
        except Exception as e:
            return f"[Error LM Studio] {e}"

    def handle_message(self, user_input: str) -> str:
        try:
            # Obtener documentos relevantes desde el retriever
            docs = self.retriever.get_relevant_documents(user_input)
            context = "\n".join([doc.page_content for doc in docs]) if docs else "No se encontró información relevante."

            # Construir prompt
            prompt = f"""
Usa la siguiente base de conocimientos para responder de forma clara y concisa:

{context}

Pregunta del usuario: {user_input}
"""
            return self.query_llm(prompt)

        except Exception as e:
            return f"[Error Chatbot] {e}"
