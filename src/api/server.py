from fastapi import FastAPI
from pydantic import BaseModel
from src.core.chatbot import Chatbot
from src.core.knowledge_base import KnowledgeBase
from src.utils.config import load_config

app = FastAPI()
config = load_config("config\config.yaml")

kb = KnowledgeBase()
kb.load_csv("data/faq.csv")
kb.load_markdown("data/knowledge.md")
retriever = kb.as_retriever()
chatbot = Chatbot(kb, retriever, config)

class ChatRequest(BaseModel):
    session_id: str
    text: str

@app.post("/chat")
def chat(req: ChatRequest):
    reply = chatbot.handle_message(req.text)
    return {"reply": reply, "handoff": False}
