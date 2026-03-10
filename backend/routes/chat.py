import asyncio
from typing import List

from fastapi import APIRouter, Depends, File, HTTPException, UploadFile
from pydantic import BaseModel
from dependencies.dependencies import get_falcon_client, get_whisper_client
from container.openvoice_container import OpenVoiceContainer
from logs.logger_singleton import Logger

logger = Logger(name="fastapi-routes")

router = APIRouter()
container = OpenVoiceContainer()


# --- pydantic  ---
class StreamlitLogsResponse(BaseModel):
    response: List[str]


class FalconResponse(BaseModel):
    response: str


# --- Routes ---
@router.post("/chat/user_upload")
async def user_upload(
    file: UploadFile = File(...),
    whisper_ai_client=Depends(get_whisper_client),
    falcon_ai_client=Depends(get_falcon_client),
):
    """
    Handle audio file upload and return AI response.
    """
    logger.info("Received request to /chat/user_upload")
    try:
        streamlit_logs = container.streamlit_logs()
        streamlit_logs.empty()

        voice_chat_service = container.create_voice_chat_service(
            whisper_client=whisper_ai_client,
            falcon_client=falcon_ai_client,
        )
        loop = asyncio.get_event_loop()
        generated_text = await loop.run_in_executor(
            None, voice_chat_service.generate, file.file
        )
        # generated_text = voice_chat_service.generate(audio_path=file.file)

        return FalconResponse(response=generated_text)

    except Exception as e:
        logger.exception("Error in /chat/user_upload")
        raise HTTPException(
            status_code=500, detail=f"Error fetching response: {str(e)}"
        )


@router.get("/chat/streamlit_logs", response_model=StreamlitLogsResponse)
async def streamlit_logs():
    """
    Handle streamlit ui logs.
    """
    logger.info("Received request to /chat/streamlit_logs")
    try:
        streamlit_logs = container.streamlit_logs()
        logs = streamlit_logs.fetch()

        return StreamlitLogsResponse(response=logs)

    except Exception as e:
        logger.exception("Error in /chat/streamlit_logs")
        raise HTTPException(
            status_code=500, detail=f"Error fetching response: {str(e)}"
        )
