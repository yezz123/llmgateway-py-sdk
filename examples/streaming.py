"""Example of using the LLMGateway client with streaming."""

import os

from examples.logger_config import setup_logger
from llmgateway import ChatCompletionRequest, LLMGatewayClient, Message

logger = setup_logger("streaming")


def main():
    """Main function."""
    # Initialize the client
    client = LLMGatewayClient(
        api_key=os.getenv("LLMGATEWAY_API_KEY", "your-api-key-here"),
    )

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
    # Get the streaming response
    for response in client.chat_completions(request):
        if response.choices[0].delta.content:
            logger.info("%s", response.choices[0].delta.content)


if __name__ == "__main__":
    main()
