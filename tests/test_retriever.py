from src.bot.retriever import FAQRetriever

def test_best_match():
    faqs = [
        {"question": "¿Tienen soporte 24/7?", "answer": "Sí, soporte 24/7.", "category": "soporte"},
        {"question": "¿Cómo solicitar una cotización?", "answer": "Escríbenos a ventas.", "category": "ventas"},
    ]
    r = FAQRetriever(faqs)
    ans, cat, score = r.best_match("¿Hay soporte todo el día?")
    assert ans is not None
    assert score >= 0.0