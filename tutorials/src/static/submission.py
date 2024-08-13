from abc import ABC, abstractmethod


class Submission(ABC):
    @abstractmethod
    def run(self, prompt: str) -> str:
        ...
