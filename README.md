# LLMGateway Python SDK

![LLMGateway Logo](https://github.com/theopenco/llmgateway/blob/main/apps/ui/static/opengraph.png?raw=true)

A Python SDK for interacting with the LLMGateway API.

---

| Project | Status                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                               |
| ------- | ---------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------- |
| CI      | [![ CI ](https://github.com/yezz123/llmgateway-py-sdk/actions/workflows/ci.yaml/badge.svg)](https://github.com/yezz123/llmgateway-py-sdk/actions/workflows/ci.yaml) [![ Pre-commit ](https://github.com/yezz123/llmgateway-py-sdk/actions/workflows/pre-commit.yaml/badge.svg)](https://github.com/yezz123/llmgateway-py-sdk/actions/workflows/pre-commit.yaml) [![ Codecov ](https://codecov.io/gh/yezz123/llmgateway-py-sdk/branch/main/graph/badge.svg)](https://codecov.io/gh/yezz123/llmgateway-py-sdk)                                                                                   |
| Meta    | [![ Package version ](https://img.shields.io/pypi/v/llmgateway-sdk?color=%2334D058&label=pypi%20package)](https://pypi.org/project/llmgateway-sdk) [![ Pydantic Version 2 ](https://img.shields.io/endpoint?url=https://raw.githubusercontent.com/pydantic/pydantic/main/docs/badge/v2.json)](https://pydantic.dev) [![ Ruff ](https://img.shields.io/endpoint?url=https://raw.githubusercontent.com/astral-sh/ruff/main/assets/badge/v2.json)](https://github.com/astral-sh/ruff) |

---

## Installation

```bash
# using pip
pip install llmgateway-sdk

# using uv
uv pip install llmgateway-sdk

# using poetry
poetry add llmgateway-sdk
```

## Usage

### Basic Usage

```python
from llmgateway import LLMGatewayClient, ChatCompletionRequest, Message

# Initialize the client
client = LLMGatewayClient(api_key="your-api-key")

# Create a chat completion request
request = ChatCompletionRequest(
    model="gpt-4",
    messages=[
        Message(role="user", content="Hello!")
    ]
)

# Get a completion
response = client.chat_completions(request)
print(response.message)

# List available models
models = client.list_models()
for model in models.data:
    print(f"Model: {model.name} (ID: {model.id})")
```

### Async Usage

```python
import asyncio
from llmgateway import LLMGatewayClient, ChatCompletionRequest, Message

async def main():
    client = LLMGatewayClient(api_key="your-api-key")

    request = ChatCompletionRequest(
        model="gpt-4",
        messages=[
            Message(role="user", content="Hello!")
        ]
    )

    # Get a completion asynchronously
    response = await client.achat_completions(request)
    print(response.message)

    # List models asynchronously
    models = await client.alist_models()
    for model in models.data:
        print(f"Model: {model.name} (ID: {model.id})")

    # Don't forget to close the client
    await client.aclose()

asyncio.run(main())
```

### Streaming Responses

```python
from llmgateway import LLMGatewayClient, ChatCompletionRequest, Message

client = LLMGatewayClient(api_key="your-api-key")

request = ChatCompletionRequest(
    model="gpt-4",
    messages=[
        Message(role="user", content="Tell me a story")
    ],
    stream=True
)

# Get streaming responses
for response in client.chat_completions(request):
    print(response.message, end="", flush=True)
```

## Features

- Synchronous and asynchronous API support
- Streaming responses
- Type hints and validation using Pydantic
- Comprehensive test coverage
- Modern Python packaging with pyproject.toml

## License

MIT License
