"""Example of using the LLMGateway client asynchronously."""

import asyncio
import os

from examples.logger_config import setup_logger
from llmgateway import ChatCompletionRequest, LLMGatewayClient, Message

logger = setup_logger("async_usage")


async def main():
    """Main function."""
    # Initialize the client
    client = LLMGatewayClient(
        api_key=os.getenv("LLMGATEWAY_API_KEY", "your-api-key-here"),
    )

    try:
        # Create a chat completion request
        request = ChatCompletionRequest(
            model="gpt-3.5-turbo",
            messages=[
                Message(role="system", content="You are a helpful assistant."),
                Message(role="user", content="What is the capital of France?"),
            ],
        )

        # Get the response asynchronously
        response = await client.achat_completions(request)
        logger.info("Assistant: %s", response.choices[0].message.content)

        # List available models asynchronously
        models = await client.alist_models()
        logger.info("Available models:")
        for model in models.data:
            logger.info("- %s", model.id)

        # Check API health asynchronously
        health = await client.ahealth_check()
        logger.info("API Health: %s", health)

    finally:
        # Always close the async client
        await client.aclose()


if __name__ == "__main__":
    asyncio.run(main())
