from abc import ABC, abstractmethod

class AIServiceInterface(ABC):

    @abstractmethod
    def analyze_email(self, content: str) -> dict:
        pass
