from src.bot.classifier import simple_rule_classifier

def test_classifier_rules():
    assert simple_rule_classifier("Necesito una cotización") == "ventas"
    assert simple_rule_classifier("Tengo un error al instalar") == "soporte"
    assert simple_rule_classifier("¿Qué servicios ofrecen?") == "información"