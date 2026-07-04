from app.ai.providers.base import BaseEmbeddingProvider, BaseLLMProvider


class MockLLMProvider(BaseLLMProvider):
    def chat(self, messages: list[dict[str, str]]) -> str:
        last = messages[-1]["content"] if messages else ""
        return f"[mock] {last}"


class MockEmbeddingProvider(BaseEmbeddingProvider):
    def embed(self, texts: list[str]) -> list[list[float]]:
        return [[0.0] * 8 for _ in texts]
