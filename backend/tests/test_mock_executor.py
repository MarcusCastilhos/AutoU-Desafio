import sys
from pathlib import Path
import json

sys.path.insert(0, str(Path(__file__).parent.parent))

from services.mock_executor import MockExecutor
from services.ai_interface import AIServiceInterface


def test_mock_executor_implements_interface():
    executor = MockExecutor()
    assert isinstance(executor, AIServiceInterface)


def test_mock_executor_productive_email():
    executor = MockExecutor()

    prompt = '''
    Analise o email abaixo:
    """
    Qual o status do meu chamado?
    """
    '''

    result = executor.execute(prompt)
    data = json.loads(result)

    assert data["category"] == "Produtivo"
    assert isinstance(data["response"], str)


def test_mock_executor_unproductive_email():
    executor = MockExecutor()

    prompt = '''
    Analise o email abaixo:
    """
    Feliz Natal!
    """
    '''

    result = executor.execute(prompt)
    data = json.loads(result)

    assert data["category"] == "Improdutivo"


def test_mock_executor_empty_email():
    executor = MockExecutor()

    prompt = '''
    Analise o email abaixo:
    """
    
    """
    '''

    result = executor.execute(prompt)
    data = json.loads(result)

    assert data["category"] == "Improdutivo"
