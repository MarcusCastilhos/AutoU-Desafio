from services.ai_interface import AIServiceInterface
import random
from typing import Dict, List
import re

class MockAIService(AIServiceInterface):
    """
    Serviço Mock de IA para análise de emails.
    
    Este serviço simula uma IA real classificando emails como Produtivo ou Improdutivo
    e gerando respostas contextuais apropriadas.
    """
    
    def __init__(self):
        # Palavras-chave para classificação
        self.productive_keywords = {
            # Problemas técnicos
            "problema", "erro", "bug", "falha", "defeito", "quebrado", "parado",
            "não funciona", "não está funcionando", "travando", "lento", "congelado",
            
            # Suporte e ajuda
            "ajuda", "suporte", "assistência", "socorro", "emergência", "urgente",
            "prioridade", "crítico", "importante", "necessito", "preciso",
            
            # Chamados e solicitações
            "chamado", "ticket", "ocorrência", "incidente", "solicitação",
            "requisição", "pedido", "demanda", "atendimento",
            
            # Status e acompanhamento
            "status", "andamento", "progresso", "atualização", "informação",
            "retorno", "resposta", "feedback", "acompanhamento",
            
            # Pagamentos e financeiro
            "pagamento", "fatura", "boleto", "conta", "cobrança", "débito",
            "vencimento", "multa", "juros", "reembolso", "estorno",
            
            # Segurança e acesso
            "senha", "login", "acesso", "bloqueado", "suspenso", "conta travada",
            "hackeado", "fraude", "segurança", "violação",
            
            # Produtos e serviços
            "entrega", "envio", "frete", "rastreamento", "produto", "serviço",
            "compra", "venda", "troca", "devolução", "garantia", "reclamação"
        }
        
        # Palavras que indicam emails improdutivos/informativos
        self.unproductive_keywords = {
            # Cumprimentos e saudações
            "olá", "oi", "bom dia", "boa tarde", "boa noite", "saudações",
            "cumprimentos", "saudações", "feliz", "parabéns", "comemoração",
            
            # Informativos gerais
            "informação", "informativo", "comunicado", "aviso", "notificação",
            "lembrete", "newsletter", "boletim", "circular", "memorando",
            
            # Agradecimentos
            "obrigado", "agradeço", "grato", "agradecimento", "valeu",
            "agradecemos", "obrigada", "gratidão",
            
            # Social/Networking
            "convite", "convido", "evento", "reunião", "encontro", "workshop",
            "palestra", "seminário", "conferência", "festividade",
            
            # Aniversários e datas
            "aniversário", "natal", "ano novo", "páscoa", "feriado", "data especial",
            "celebração", "comemoração", "festa",
            
            # Newsletter/Spam
            "promoção", "oferta", "desconto", "black friday", "cyber monday",
            "novidade", "lançamento", "marketing", "propaganda"
        }
        
        # Respostas para emails produtivos (organizadas por categoria)
        self.productive_responses = {
            "tecnico": [
                "Nossa equipe técnica já foi notificada sobre o problema. Iremos analisar e retornar com uma solução em até 24 horas úteis.",
                "Identificamos a questão técnica relatada. Nossa equipe especializada está trabalhando na resolução. Atualizaremos você em breve.",
                "O problema foi registrado em nosso sistema de incidentes com prioridade. Esperamos resolver isso rapidamente.",
                "Entendemos o impacto deste erro. Estamos investigando a causa raiz e implementaremos uma correção permanente."
            ],
            "suporte": [
                "Recebemos sua solicitação de suporte. Um de nossos especialistas entrará em contato em até 2 horas úteis.",
                "Sua necessidade de assistência foi registrada. Iremos priorizar seu atendimento considerando a urgência mencionada.",
                "Nossa equipe de suporte está analisando seu caso. Retornaremos com orientações específicas para resolver sua situação.",
                "Atribuímos um técnico dedicado para seu atendimento. Você receberá um contato direto em breve."
            ],
            "chamado": [
                "Seu chamado foi atualizado em nosso sistema e está sendo tratado pela equipe responsável. Número de protocolo: #{rand_num}.",
                "O status do seu chamado foi verificado e está em andamento. Iremos monitorar até a conclusão completa.",
                "Registramos sua solicitação no sistema de chamados. A previsão de resolução é de {dias} dias úteis.",
                "Seu ticket foi priorizado e está na fila de atendimento. Você receberá atualizações regulares sobre o progresso."
            ],
            "financeiro": [
                "Sua questão financeira foi encaminhada ao departamento responsável. Eles analisarão os detalhes e retornarão com esclarecimentos.",
                "Recebemos sua solicitação relacionada a pagamentos. Iremos verificar os registros e retornar com uma resposta detalhada.",
                "O setor financeiro foi notificado sobre sua demanda. Eles entrarão em contato para resolver esta questão específica.",
                "Sua solicitação financeira está sendo processada. O prazo para análise completa é de 3 dias úteis."
            ],
            "acesso": [
                "Sua questão de acesso/login foi registrada. Iremos redefinir suas credenciais e enviar instruções por email seguro.",
                "Identificamos o problema de acesso. Nossa equipe de segurança está trabalhando para restaurar seu login com segurança.",
                "O bloqueio da sua conta foi verificado. Estamos tomando as medidas necessárias para liberar o acesso o mais rápido possível.",
                "Recebemos seu relato sobre problemas de acesso. Iremos validar sua identidade e restaurar o acesso em até 1 hora útil."
            ],
            "produto": [
                "Sua solicitação relacionada ao produto/serviço foi encaminhada à equipe responsável. Eles avaliarão as possibilidades de atendimento.",
                "Recebemos seu pedido sobre nosso produto. Iremos analisar a viabilidade e retornar com opções disponíveis.",
                "Sua demanda sobre o serviço foi registrada. Nossa equipe comercial entrará em contato para discutir as alternativas.",
                "A questão com o produto foi documentada. Iremos investigar e propor uma solução adequada às suas necessidades."
            ],
            "geral": [
                "Sua mensagem foi recebida e está sendo processada pela equipe responsável. Retornaremos em breve com mais informações.",
                "Agradecemos seu contato. Iremos analisar sua solicitação e retornar com uma resposta apropriada.",
                "Recebemos sua comunicação e a encaminhamos para o setor competente. Aguarde nosso retorno.",
                "Sua demanda foi registrada em nosso sistema. Iremos tratá-la conforme as prioridades estabelecidas."
            ]
        }
        
        # Respostas para emails improdutivos
        self.unproductive_responses = [
            "Agradecemos seu contato e a mensagem informativa. Ficamos à disposição para qualquer necessidade futura.",
            "Obrigado por compartilhar esta informação conosco. Vamos arquivá-la para referência da equipe.",
            "Recebemos sua comunicação e a registramos em nosso sistema. Agradecemos a iniciativa de nos manter informados.",
            "Agradecemos a mensagem. Ficamos felizes em receber suas comunicações e manter este canal aberto.",
            "Obrigado pelo email. Sua mensagem foi recebida e arquivada para conhecimento da equipe responsável.",
            "Agradecemos o compartilhamento desta informação. Estamos sempre disponíveis para receber suas comunicações.",
            "Recebemos e registramos seu email informativo. Agradecemos por nos manter atualizados.",
            "Obrigado pela mensagem. Ficamos contentes em receber seu contato, mesmo que apenas informativo."
        ]
        
        # Padrões regex para detecção mais avançada
        self.patterns = {
            "urgencia": re.compile(r'\b(urgente|emergência|imediato|agora|hoje|rápido|priority)\b', re.IGNORECASE),
            "numero_chamado": re.compile(r'\b(chamado|ticket|protocolo)[:\s]*#?(\d+)\b', re.IGNORECASE),
            "problema_tecnico": re.compile(r'\b(erro|bug|falha|não funciona|trav[aá]|congel|parou)\b.*\b(sistema|aplicativo|site|plataforma|login)\b', re.IGNORECASE),
            "prazo": re.compile(r'\b(prazo|deadline|entrega|data|vencimento)\b.*\b(\d{1,2}[/-]\d{1,2}[/-]\d{2,4}|\d{1,2}\s+de\s+\w+)\b', re.IGNORECASE),
            "valor": re.compile(r'\b(R\$\s*\d+[,.]?\d*|\d+[,.]?\d*\s*reais|valor|preço|custo)\b', re.IGNORECASE)
        }

    def analyze_email(self, email_text: str) -> Dict[str, str]:
        """
        Analisa o conteúdo de um email e retorna categoria e resposta.
        
        Args:
            email_text: Texto completo do email
            
        Returns:
            Dict com 'category' (Produtivo/Improdutivo) e 'response' (resposta gerada)
        """
        # Limpa e normaliza o texto
        text = email_text.lower().strip()
        
        if not text:
            return self._generate_unproductive_response("vazio")
        
        # Análise de características do email
        characteristics = self._analyze_characteristics(text)
        
        # Determina categoria baseada nas características
        category = self._determine_category(characteristics)
        
        # Gera resposta apropriada
        response = self._generate_response(category, characteristics, text)
        
        return {
            "category": category,
            "response": response
        }
    
    def _analyze_characteristics(self, text: str) -> Dict[str, any]:
        """Analisa características específicas do email."""
        characteristics = {
            "has_productive_keywords": False,
            "has_unproductive_keywords": False,
            "productive_count": 0,
            "unproductive_count": 0,
            "urgency_level": 0,
            "has_technical_issue": False,
            "has_financial_content": False,
            "has_access_issue": False,
            "has_product_request": False,
            "email_length": len(text),
            "has_call_number": False,
            "call_number": None,
            "has_deadline": False,
            "has_monetary_value": False
        }
        
        # Contagem de palavras-chave
        for word in text.split():
            word_clean = word.strip('.,!?;:()[]{}"\'').lower()
            
            if word_clean in self.productive_keywords:
                characteristics["productive_count"] += 1
                characteristics["has_productive_keywords"] = True
                
                # Detecção de categorias específicas
                if word_clean in {"erro", "bug", "falha", "problema", "não funciona"}:
                    characteristics["has_technical_issue"] = True
                elif word_clean in {"pagamento", "fatura", "boleto", "conta", "reembolso"}:
                    characteristics["has_financial_content"] = True
                elif word_clean in {"senha", "login", "acesso", "bloqueado"}:
                    characteristics["has_access_issue"] = True
                elif word_clean in {"produto", "serviço", "entrega", "compra", "troca"}:
                    characteristics["has_product_request"] = True
                    
            elif word_clean in self.unproductive_keywords:
                characteristics["unproductive_count"] += 1
                characteristics["has_unproductive_keywords"] = True
        
        # Verificação de padrões regex
        if self.patterns["urgencia"].search(text):
            characteristics["urgency_level"] = 2 if "urgente" in text or "emergência" in text else 1
        
        call_match = self.patterns["numero_chamado"].search(text)
        if call_match:
            characteristics["has_call_number"] = True
            characteristics["call_number"] = call_match.group(2)
        
        if self.patterns["problema_tecnico"].search(text):
            characteristics["has_technical_issue"] = True
        
        if self.patterns["prazo"].search(text):
            characteristics["has_deadline"] = True
        
        if self.patterns["valor"].search(text):
            characteristics["has_monetary_value"] = True
        
        return characteristics
    
    def _determine_category(self, characteristics: Dict[str, any]) -> str:
        """Determina a categoria baseada nas características analisadas."""
        
        # Regras de classificação
        productive_score = 0
        unproductive_score = 0
        
        # Pontuação para características produtivas
        productive_score += characteristics["productive_count"] * 2
        productive_score += characteristics["urgency_level"] * 3
        if characteristics["has_technical_issue"]:
            productive_score += 5
        if characteristics["has_financial_content"]:
            productive_score += 4
        if characteristics["has_access_issue"]:
            productive_score += 4
        if characteristics["has_call_number"]:
            productive_score += 3
        if characteristics["has_deadline"]:
            productive_score += 2
        if characteristics["has_monetary_value"]:
            productive_score += 3
        
        # Pontuação para características improdutivas
        unproductive_score += characteristics["unproductive_count"] * 2
        if characteristics["email_length"] < 50:  # Emails muito curtos tendem a ser informativos
            unproductive_score += 3
        if "obrigado" in characteristics or "agrade" in characteristics:
            unproductive_score += 4
        
        # Decisão final
        if productive_score > unproductive_score:
            return "Produtivo"
        elif productive_score == unproductive_score and productive_score > 0:
            # Empate com algum conteúdo - tende para produtivo
            return "Produtivo"
        else:
            return "Improdutivo"
    
    def _generate_response(self, category: str, characteristics: Dict[str, any], original_text: str) -> str:
        """Gera uma resposta apropriada baseada na categoria e características."""
        
        if category == "Produtivo":
            return self._generate_productive_response(characteristics, original_text)
        else:
            return self._generate_unproductive_response(characteristics)
    
    def _generate_productive_response(self, characteristics: Dict[str, any], original_text: str) -> str:
        """Gera resposta para email produtivo."""
        
        # Determina o tipo específico de resposta
        response_type = "geral"
        
        if characteristics["has_technical_issue"]:
            response_type = "tecnico"
        elif characteristics["has_access_issue"]:
            response_type = "acesso"
        elif characteristics["has_financial_content"]:
            response_type = "financeiro"
        elif characteristics["has_product_request"]:
            response_type = "produto"
        elif characteristics["has_call_number"]:
            response_type = "chamado"
        elif "suporte" in original_text or "ajuda" in original_text:
            response_type = "suporte"
        
        # Seleciona resposta aleatória do tipo apropriado
        response_template = random.choice(self.productive_responses[response_type])
        
        # Personaliza a resposta
        response = self._personalize_response(response_template, characteristics, original_text)
        
        return response
    
    def _generate_unproductive_response(self, characteristics) -> str:
        """Gera resposta para email improdutivo."""
        return random.choice(self.unproductive_responses)
    
    def _personalize_response(self, template: str, characteristics: Dict[str, any], original_text: str) -> str:
        """Personaliza a resposta com informações específicas."""
        
        response = template
        
        # Adiciona número de protocolo se detectado
        if characteristics["has_call_number"] and characteristics["call_number"]:
            response = response.replace("{rand_num}", characteristics["call_number"])
        else:
            rand_num = random.randint(1000, 9999)
            response = response.replace("{rand_num}", str(rand_num))
        
        # Adiciona prazo estimado se relevante
        if "{dias}" in response:
            if characteristics["urgency_level"] >= 2:
                dias = random.randint(1, 2)
            elif characteristics["has_technical_issue"]:
                dias = random.randint(2, 5)
            else:
                dias = random.randint(3, 7)
            response = response.replace("{dias}", str(dias))
        
        # Adiciona menção à urgência se detectada
        if characteristics["urgency_level"] >= 2 and "urgent" not in response.lower():
            urgency_phrases = [
                " Devido à urgência mencionada, priorizaremos seu atendimento.",
                " Considerando a natureza urgente, aceleraremos o processo.",
                " Entendemos a urgência e estamos tratando com prioridade máxima."
            ]
            response += random.choice(urgency_phrases)
        
        return response
    
    def batch_analyze(self, emails: List[str]) -> List[Dict[str, str]]:
        """
        Analisa múltiplos emails de uma vez (para testes de carga/performance).
        
        Args:
            emails: Lista de textos de email
            
        Returns:
            Lista de dicts com análise de cada email
        """
        return [self.analyze_email(email) for email in emails]
    
    def get_stats(self, emails: List[str]) -> Dict[str, any]:
        """
        Retorna estatísticas sobre uma lista de emails.
        
        Args:
            emails: Lista de textos de email
            
        Returns:
            Dict com estatísticas de análise
        """
        if not emails:
            return {
                "total_emails": 0,
                "productive_count": 0,
                "unproductive_count": 0,
                "productive_percentage": 0,
                "avg_email_length": 0
            }
        
        analyses = self.batch_analyze(emails)
        
        productive_count = sum(1 for a in analyses if a["category"] == "Produtivo")
        total_chars = sum(len(email) for email in emails)
        
        return {
            "total_emails": len(emails),
            "productive_count": productive_count,
            "unproductive_count": len(emails) - productive_count,
            "productive_percentage": (productive_count / len(emails)) * 100,
            "avg_email_length": total_chars / len(emails)
        }


# Exemplo de uso para testes
if __name__ == "__main__":
    service = MockAIService()
    
    # Testes básicos
    test_emails = [
        "URGENTE: Sistema travado, não consigo acessar minhas faturas!",
        "Olá, bom dia a todos! Apenas passando para desejar um ótimo final de semana.",
        "Meu chamado #4567 está parado há 3 dias. Preciso de uma solução imediata.",
        "Obrigado pelo excelente atendimento na reunião de hoje.",
        "Erro 500 ao tentar fazer login no painel administrativo.",
        "Gostaria de solicitar o reembolso da compra #789, no valor de R$ 450,00.",
        "Convido todos para a festa de aniversário da empresa na próxima sexta.",
        "Senha expirada, não consigo acessar minha conta. É urgente!"
    ]
    
    print("📧 Teste do MockAIService - Análise de Emails\n")
    print("=" * 60)
    
    for i, email in enumerate(test_emails, 1):
        result = service.analyze_email(email)
        print(f"Email {i}:")
        print(f"  Conteúdo: {email[:50]}...")
        print(f"  Categoria: {result['category']}")
        print(f"  Resposta: {result['response']}")
        print("-" * 60)
    
    # Estatísticas
    stats = service.get_stats(test_emails)
    print("\n📊 Estatísticas Gerais:")
    print(f"  Total de emails: {stats['total_emails']}")
    print(f"  Produtivos: {stats['productive_count']} ({stats['productive_percentage']:.1f}%)")
    print(f"  Improdutivos: {stats['unproductive_count']}")
    print(f"  Comprimento médio: {stats['avg_email_length']:.0f} caracteres")