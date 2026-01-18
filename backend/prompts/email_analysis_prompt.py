def build_email_analysis_prompt(email_text: str) -> str:
    return f"""
Você é um sistema que classifica emails corporativos.

Classifique o email abaixo em:
- Produtivo
- Improdutivo

Depois gere uma resposta automática adequada.

Retorne SOMENTE um JSON válido no formato:
{{
  "category": "Produtivo ou Improdutivo",
  "response": "Texto da resposta automática"
}}

Email:
\"\"\"{email_text}\"\"\"
"""
