from abc import ABC, abstractmethod
from collections.abc import Iterable


class BaseLLMProvider(ABC):
    @abstractmethod
    def chat(self, messages: list[dict[str, str]]) -> str:
        raise NotImplementedError

    def stream_chat(self, messages: list[dict[str, str]]) -> Iterable[str]:
        yield self.chat(messages)


class BaseEmbeddingProvider(ABC):
    @abstractmethod
    def embed(self, texts: list[str]) -> list[list[float]]:
        raise NotImplementedError
