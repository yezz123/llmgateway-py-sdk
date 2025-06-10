"""Example of using the LLMGateway client with async streaming."""

import asyncio
import os

from examples.logger_config import setup_logger
from llmgateway import ChatCompletionRequest, LLMGatewayClient, Message

logger = setup_logger("async_streaming")


async def main():
    """Main function."""
    # Initialize the client
    client = LLMGatewayClient(
        api_key=os.getenv("LLMGATEWAY_API_KEY", "your-api-key-here"),
    )

    try:
        # Create a streaming chat completion request
        request = ChatCompletionRequest(
            model="gpt-3.5-turbo",
            messages=[
                Message(role="system", content="You are a helpful assistant."),
                Message(role="user", content="Write a short poem about programming."),
            ],
            stream=True,  # Enable streaming
        )

        logger.info("Assistant: ")
        # Get the streaming response asynchronously
        async for response in client.achat_completions(request):
            if response.choices[0].delta.content:
                logger.info("%s", response.choices[0].delta.content)

    finally:
        # Always close the async client
        await client.aclose()


if __name__ == "__main__":
    asyncio.run(main())
