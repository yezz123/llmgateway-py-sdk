"""LLMGateway API client."""

import json
from collections.abc import AsyncGenerator, Generator
from typing import Any, Optional, TypeVar, Union

import httpx

from .models import (
    ChatCompletionRequest,
    ChatCompletionResponse,
    ModelList,
)

T = TypeVar("T")


class LLMGatewayClient:
    """Client for interacting with the LLMGateway API."""

    def __init__(
        self,
        api_key: str,
        base_url: str = "https://api.llmgateway.io",
        timeout: float = 30.0,
    ) -> None:
        """Initialize the LLMGateway client.

        Args:
            api_key: Your LLMGateway API key
            base_url: The base URL for the API
            timeout: Request timeout in seconds
        """
        self.api_key = api_key
        self.base_url = base_url.rstrip("/")
        self.timeout = timeout
        self._client = httpx.Client(
            base_url=self.base_url,
            timeout=timeout,
            headers={"Authorization": f"Bearer {api_key}"},
        )
        self._async_client = httpx.AsyncClient(
            base_url=self.base_url,
            timeout=timeout,
            headers={"Authorization": f"Bearer {api_key}"},
        )

    def __enter__(self) -> "LLMGatewayClient":
        """Enter the context manager."""
        return self

    def __exit__(
        self, exc_type: Optional[type[BaseException]], exc_val: Optional[BaseException], exc_tb: Optional[Any]
    ) -> None:
        """Exit the context manager."""
        self.close()

    def close(self) -> None:
        """Close the HTTP client."""
        self._client.close()

    async def aclose(self) -> None:
        """Close the async HTTP client."""
        await self._async_client.aclose()

    def health_check(self) -> dict[str, Any]:
        """Check the health of the API.

        Returns:
            Dict containing health check information
        """
        response = self._client.get("/")
        _ = response.raise_for_status()
        return response.json()

    async def ahealth_check(self) -> dict[str, Any]:
        """Async version of health_check."""
        response = await self._async_client.get("/")
        _ = await response.raise_for_status()  # type: ignore
        return await response.json()

    def chat_completions(
        self,
        request: ChatCompletionRequest,
    ) -> Union[ChatCompletionResponse, Generator[ChatCompletionResponse, None, None]]:
        """Create a chat completion.

        Args:
            request: The chat completion request

        Returns:
            ChatCompletionResponse or Generator for streaming responses
        """
        if request.stream:
            return self._stream_chat_completions(request)

        response = self._client.post(
            "/v1/chat/completions",
            json=request.model_dump(exclude_none=True),
        )
        _ = response.raise_for_status()
        return ChatCompletionResponse(**response.json())

    async def achat_completions(
        self,
        request: ChatCompletionRequest,
    ) -> Union[ChatCompletionResponse, AsyncGenerator[ChatCompletionResponse, None]]:
        """Async version of chat_completions."""
        if request.stream:
            return self._astream_chat_completions(request)

        response = await self._async_client.post(
            "/v1/chat/completions",
            json=request.model_dump(exclude_none=True),
        )
        _ = await response.raise_for_status()  # type: ignore
        return ChatCompletionResponse(**await response.json())

    def _stream_chat_completions(
        self,
        request: ChatCompletionRequest,
    ) -> Generator[ChatCompletionResponse, None, None]:
        """Stream chat completions."""
        with self._client.stream(
            "POST",
            "/v1/chat/completions",
            json=request.model_dump(exclude_none=True),
        ) as response:
            _ = response.raise_for_status()
            for line in response.iter_lines():
                if line:
                    if isinstance(line, bytes):
                        line = line.decode()
                    data = json.loads(line)
                    yield ChatCompletionResponse(**data)

    async def _astream_chat_completions(
        self,
        request: ChatCompletionRequest,
    ) -> AsyncGenerator[ChatCompletionResponse, None]:
        """Async stream chat completions."""
        async with self._async_client.stream(
            "POST",
            "/v1/chat/completions",
            json=request.model_dump(exclude_none=True),
        ) as response:
            _ = await response.raise_for_status()  # type: ignore
            async for line in response.aiter_lines():
                if line:
                    if isinstance(line, bytes):
                        line = line.decode()
                    data = json.loads(line)
                    yield ChatCompletionResponse(**data)

    def list_models(self) -> ModelList:
        """List all available models.

        Returns:
            ModelList containing available models
        """
        response = self._client.get("/v1/models")
        _ = response.raise_for_status()
        return ModelList(**response.json())

    async def alist_models(self) -> ModelList:
        """Async version of list_models."""
        response = await self._async_client.get("/v1/models")
        _ = await response.raise_for_status()  # type: ignore
        return ModelList(**await response.json())
