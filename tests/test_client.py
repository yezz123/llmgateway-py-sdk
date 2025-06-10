"""Tests for the LLMGateway client."""

from unittest.mock import AsyncMock

import httpx
import pytest

from llmgateway import LLMGatewayClient
from llmgateway.models import (
    ChatCompletionRequest,
    Message,
    ModelList,
)


@pytest.fixture
def api_key():
    """Fixture for the API key."""
    return "test-api-key"


@pytest.fixture
def client(api_key):
    """Fixture for the LLMGateway client."""
    return LLMGatewayClient(api_key=api_key)


@pytest.fixture
def mock_response():
    """Fixture for the mock response."""
    return {
        "message": "Hello!",
        "health": {
            "status": "ok",
            "redis": {"connected": True},
            "database": {"connected": True},
        },
    }


@pytest.fixture
def mock_models_response():
    """Fixture for the mock models response."""
    return {
        "data": [
            {
                "id": "gpt-4",
                "name": "GPT-4",
                "created": 1677610602,
                "architecture": {
                    "input_modalities": ["text"],
                    "output_modalities": ["text"],
                },
                "top_provider": {"is_moderated": True},
                "providers": [
                    {
                        "providerId": "openai",
                        "modelName": "gpt-4",
                        "pricing": {
                            "prompt": "0.03",
                            "completion": "0.06",
                        },
                    }
                ],
                "pricing": {
                    "prompt": "0.03",
                    "completion": "0.06",
                },
            }
        ]
    }


def test_client_initialization(api_key):
    """Test the client initialization."""
    client = LLMGatewayClient(api_key=api_key)
    assert client.api_key == api_key
    assert client.base_url == "https://api.llmgateway.io"
    assert client.timeout == 30.0


def test_health_check(client, mock_response):
    """Test the health check."""

    def handler(request):
        return httpx.Response(200, json=mock_response)

    transport = httpx.MockTransport(handler)
    client._client = httpx.Client(transport=transport, base_url=client.base_url)
    response = client.health_check()
    assert response == mock_response


def test_chat_completions(client):
    """Test the chat completions."""

    def handler(request):
        return httpx.Response(200, json={"message": "Hello! How can I help you?"})

    transport = httpx.MockTransport(handler)
    client._client = httpx.Client(transport=transport, base_url=client.base_url)
    request_obj = ChatCompletionRequest(
        model="gpt-4",
        messages=[Message(role="user", content="Hello!")],
    )
    response = client.chat_completions(request_obj)
    assert response.message == "Hello! How can I help you?"


def test_chat_completions_streaming(client):
    """Test the chat completions streaming."""

    def handler(request):
        # Simulate a streaming response with proper bytes
        content = b'{"message": "Hello!"}\n{"message": "How can I help you?"}'
        return httpx.Response(200, content=content, headers={"transfer-encoding": "chunked"})

    transport = httpx.MockTransport(handler)
    client._client = httpx.Client(transport=transport, base_url=client.base_url)
    request_obj = ChatCompletionRequest(
        model="gpt-4",
        messages=[Message(role="user", content="Hello!")],
        stream=True,
    )
    responses = list(client.chat_completions(request_obj))
    assert len(responses) == 2
    assert responses[0].message == "Hello!"
    assert responses[1].message == "How can I help you?"


def test_list_models(client, mock_models_response):
    """Test the list models."""

    def handler(request):
        return httpx.Response(200, json=mock_models_response)

    transport = httpx.MockTransport(handler)
    client._client = httpx.Client(transport=transport, base_url=client.base_url)
    response = client.list_models()
    assert isinstance(response, ModelList)
    assert len(response.data) == 1
    assert response.data[0].id == "gpt-4"
    assert response.data[0].name == "GPT-4"


@pytest.mark.asyncio
async def test_async_health_check(client, mock_response):
    """Test the async health check."""

    async def handler(request):
        resp = httpx.Response(200, json=mock_response)
        resp.raise_for_status = AsyncMock()
        resp.json = AsyncMock(return_value=mock_response)
        return resp

    transport = httpx.MockTransport(handler)
    client._async_client = httpx.AsyncClient(transport=transport, base_url=client.base_url)
    response = await client.ahealth_check()
    assert response == mock_response


@pytest.mark.asyncio
async def test_async_chat_completions(client):
    """Test the async chat completions."""

    async def handler(request):
        data = {"message": "Hello! How can I help you?"}
        resp = httpx.Response(200, json=data)
        resp.raise_for_status = AsyncMock()
        resp.json = AsyncMock(return_value=data)
        return resp

    transport = httpx.MockTransport(handler)
    client._async_client = httpx.AsyncClient(transport=transport, base_url=client.base_url)
    request_obj = ChatCompletionRequest(
        model="gpt-4",
        messages=[Message(role="user", content="Hello!")],
    )
    response = await client.achat_completions(request_obj)
    assert response.message == "Hello! How can I help you?"


@pytest.mark.asyncio
async def test_async_chat_completions_streaming(client):
    """Test the async chat completions streaming."""

    async def handler(request):
        content = b'{"message": "Hello!"}\n{"message": "How can I help you?"}'
        resp = httpx.Response(200, content=content, headers={"transfer-encoding": "chunked"})
        resp.raise_for_status = AsyncMock()
        return resp

    transport = httpx.MockTransport(handler)
    client._async_client = httpx.AsyncClient(transport=transport, base_url=client.base_url)
    request_obj = ChatCompletionRequest(
        model="gpt-4",
        messages=[Message(role="user", content="Hello!")],
        stream=True,
    )
    responses = []
    async for response in await client.achat_completions(request_obj):
        responses.append(response)
    assert len(responses) == 2
    assert responses[0].message == "Hello!"
    assert responses[1].message == "How can I help you?"


@pytest.mark.asyncio
async def test_async_list_models(client, mock_models_response):
    """Test the async list models."""

    async def handler(request):
        resp = httpx.Response(200, json=mock_models_response)
        resp.raise_for_status = AsyncMock()
        resp.json = AsyncMock(return_value=mock_models_response)
        return resp

    transport = httpx.MockTransport(handler)
    client._async_client = httpx.AsyncClient(transport=transport, base_url=client.base_url)
    response = await client.alist_models()
    assert isinstance(response, ModelList)
    assert len(response.data) == 1
    assert response.data[0].id == "gpt-4"
    assert response.data[0].name == "GPT-4"
