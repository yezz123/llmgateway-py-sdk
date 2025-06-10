"""Basic example of using the LLMGateway client synchronously."""

import os

from examples.logger_config import setup_logger
from llmgateway import ChatCompletionRequest, LLMGatewayClient, Message

logger = setup_logger("basic_usage")


def main():
    """Main function."""
    # Initialize the client
    client = LLMGatewayClient(
        api_key=os.getenv("LLMGATEWAY_API_KEY", "your-api-key-here"),
    )

    # Create a chat completion request
    request = ChatCompletionRequest(
        model="gpt-3.5-turbo",
        messages=[
            Message(role="system", content="You are a helpful assistant."),
            Message(role="user", content="What is the capital of France?"),
        ],
    )

    # Get the response
    response = client.chat_completions(request)
    logger.info("Assistant: %s", response.choices[0].message.content)

    # List available models
    models = client.list_models()
    logger.info("Available models:")
    for model in models.data:
        logger.info("- %s", model.id)

    # Check API health
    health = client.health_check()
    logger.info("API Health: %s", health)


if __name__ == "__main__":
    main()
