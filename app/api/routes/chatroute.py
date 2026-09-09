from fastapi import APIRouter, HTTPException
from app.schemas.chatmodelschema import (
    ChatMessageCreate,
    ChatMessageResponse
)
from app.logging.logger import logger
from app.graph.workflow import app

router = APIRouter(
    prefix="/chat",
    tags=["Chat"]
)
@router.post(
    "/",
    response_model=ChatMessageResponse
)
async def chat(message: ChatMessageCreate):
    try:
        operation_keys = {
            "summarize": "summarized_text",
            "explain": "explain_text",
            "translate": "translate_text",
            "podcast": "podcast",
        }
        response_key = operation_keys.get(message.operation)
        if response_key is None:
            raise HTTPException(
                status_code=422,
                detail="Operation must be summarize, explain, translate, or podcast."
            )
        initial_state = {
            "text": message.text,
            "summarized_text": "",
            "explain_text": "",
            "translate_text": "",
            "podcast": "",
            "target_language": message.target_language,
            "operation": message.operation
        }
        result = await app.ainvoke(initial_state)
        response_text = result.get(
            response_key,
            ""
        )
        if not response_text:
            logger.error(f"The workflow did not return a response.")
            raise HTTPException(
                status_code=500,
                detail="The workflow did not return a response."
            )
        return ChatMessageResponse(
            text=response_text
        )
    except HTTPException:
        raise
    except Exception as error:
        logger.critical(f"{str(error)}")
        raise HTTPException(
            status_code=500,
            detail=str(error)
        )