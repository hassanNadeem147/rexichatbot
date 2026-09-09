from pydantic import BaseModel, ConfigDict, Field
class ChatMessageCreate(BaseModel):
    text: str = Field(
        ...,
        description="The content of the chat message"
    )
    operation: str = Field(
        ...,
        description="The operation to perform"
    )
    target_language: str = Field(
        ...,
        description="The target language for the operation"
    )
class ChatMessageResponse(BaseModel):
    text: str = Field(
        ...,
        description="The chatbot response"
    )