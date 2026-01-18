import random
import re
from typing import Dict, List


class MockAIService:
    def __init__(self):
        self.productive_keywords = {
            "problema", "erro", "bug", "falha", "defeito", "quebrado", "parado",
            "ajuda", "suporte", "urgente", "prioridade", "chamado", "ticket",
            "pagamento", "fatura", "boleto", "senha", "login", "acesso",
            "entrega", "produto", "serviço", "reembolso", "troca"
        }

        self.unproductive_keywords = {
            "olá", "oi", "bom dia", "boa tarde", "boa noite",
            "obrigado", "agradeço", "parabéns", "feliz",
            "newsletter", "promoção", "oferta", "convite"
        }

        self.productive_responses = [
            "Recebemos sua solicitação e ela já está sendo analisada.",
            "Sua demanda foi registrada e encaminhada para o setor responsável.",
            "Identificamos a necessidade e retornaremos com uma solução em breve.",
            "Sua solicitação foi priorizada e está em andamento."
        ]

        self.unproductive_responses = [
            "Agradecemos a mensagem e ficamos à disposição.",
            "Obrigado pelo contato! Registramos sua comunicação.",
            "Mensagem recebida. Qualquer necessidade adicional, nos avise."
        ]

        self.patterns = {
            "urgencia": re.compile(r"\b(urgente|emergência|imediato)\b", re.IGNORECASE),
            "chamado": re.compile(r"\b(chamado|ticket|protocolo)\s*#?\d+", re.IGNORECASE),
        }

    def analyze_email(self, email_text: str) -> Dict[str, str]:
        text = email_text.lower().strip()

        if not text:
            return self._unproductive_response()

        productive_score = self._calculate_productive_score(text)
        unproductive_score = self._calculate_unproductive_score(text)

        if productive_score >= unproductive_score:
            return self._productive_response()
        else:
            return self._unproductive_response()

    def _calculate_productive_score(self, text: str) -> int:
        score = 0

        for word in self.productive_keywords:
            if word in text:
                score += 2

        if self.patterns["urgencia"].search(text):
            score += 3

        if self.patterns["chamado"].search(text):
            score += 2

        return score

    def _calculate_unproductive_score(self, text: str) -> int:
        score = 0

        for word in self.unproductive_keywords:
            if word in text:
                score += 2

        if len(text) < 40:
            score += 2

        return score

    def _productive_response(self) -> Dict[str, str]:
        return {
            "category": "Produtivo",
            "response": random.choice(self.productive_responses),
        }

    def _unproductive_response(self) -> Dict[str, str]:
        return {
            "category": "Improdutivo",
            "response": random.choice(self.unproductive_responses),
        }

    def batch_analyze(self, emails: List[str]) -> List[Dict[str, str]]:
        return [self.analyze_email(email) for email in emails]
