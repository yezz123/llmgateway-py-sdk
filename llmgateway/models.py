"""Pydantic models for LLMGateway API."""

from typing import Any, Optional

from pydantic import BaseModel, Field


class Message(BaseModel):
    """A message in a chat conversation."""

    role: str
    content: str


class ResponseFormat(BaseModel):
    """Response format configuration."""

    type: str = Field(pattern="^(text|json_object)$")


class ChatCompletionRequest(BaseModel):
    """Request model for chat completions."""

    model: str
    messages: list[Message]
    temperature: Optional[float] = None
    max_tokens: Optional[int] = None
    top_p: Optional[float] = None
    frequency_penalty: Optional[float] = None
    presence_penalty: Optional[float] = None
    response_format: Optional[ResponseFormat] = None
    stream: bool = False


class ChatCompletionResponse(BaseModel):
    """Response model for chat completions."""

    message: str


class ErrorResponse(BaseModel):
    """Error response model."""

    error: dict[str, Any]


class Architecture(BaseModel):
    """Model architecture information."""

    input_modalities: list[str]
    output_modalities: list[str]
    tokenizer: Optional[str] = None


class TopProvider(BaseModel):
    """Top provider information."""

    is_moderated: bool


class ProviderPricing(BaseModel):
    """Provider pricing information."""

    prompt: str
    completion: str
    image: Optional[str] = None


class Provider(BaseModel):
    """Provider information."""

    providerId: str
    modelName: str
    pricing: ProviderPricing


class ModelPricing(BaseModel):
    """Model pricing information."""

    prompt: str
    completion: str
    image: Optional[str] = None
    request: Optional[str] = None
    input_cache_read: Optional[str] = None
    input_cache_write: Optional[str] = None
    web_search: Optional[str] = None
    internal_reasoning: Optional[str] = None


class Model(BaseModel):
    """Model information."""

    id: str
    name: str
    created: int
    description: Optional[str] = None
    architecture: Architecture
    top_provider: TopProvider
    providers: list[Provider]
    pricing: ModelPricing
    context_length: Optional[int] = None
    hugging_face_id: Optional[str] = None
    per_request_limits: Optional[dict[str, str]] = None
    supported_parameters: Optional[list[str]] = None


class ModelList(BaseModel):
    """List of available models."""

    data: list[Model]
