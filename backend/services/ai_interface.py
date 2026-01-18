from abc import ABC, abstractmethod

class AIServiceInterface(ABC):

    @abstractmethod
    def execute(self, prompt: str) -> str:
        pass
