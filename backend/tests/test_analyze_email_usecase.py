import os
import sys
import json
import pytest
from pathlib import Path

# Garante import do projeto
sys.path.insert(0, str(Path(__file__).parent.parent))

from usecases.analyze_email_usecase import AnalyzeEmailUseCase


@pytest.mark.asyncio
async def test_usecase_productive_email():
    os.environ["USE_MOCK_AI"] = "true"

    usecase = AnalyzeEmailUseCase()

    result = await usecase.execute("Preciso de suporte técnico urgente")

    assert isinstance(result, dict)
    assert result["category"] == "Produtivo"
    assert isinstance(result["response"], str)


@pytest.mark.asyncio
async def test_usecase_unproductive_email():
    os.environ["USE_MOCK_AI"] = "true"

    usecase = AnalyzeEmailUseCase()

    result = await usecase.execute("Feliz Natal a todos!")

    assert result["category"] == "Improdutivo"


@pytest.mark.asyncio
async def test_usecase_empty_email():
    os.environ["USE_MOCK_AI"] = "true"

    usecase = AnalyzeEmailUseCase()

    result = await usecase.execute("")

    assert result["category"] == "Improdutivo"


@pytest.mark.asyncio
async def test_usecase_returns_expected_contract():
    os.environ["USE_MOCK_AI"] = "true"

    usecase = AnalyzeEmailUseCase()

    result = await usecase.execute("Teste qualquer")

    assert isinstance(result, dict)
    assert "category" in result
    assert "response" in result
