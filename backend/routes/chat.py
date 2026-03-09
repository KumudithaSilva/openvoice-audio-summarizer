from fastapi import APIRouter, Depends, File, HTTPException, UploadFile
from dependencies.dependencies import get_falcon_client, get_whisper_client
from container.openvoice_container import OpenVoiceContainer
from logs.logger_singleton import Logger

logger = Logger(name="fastapi-routes")

router = APIRouter()
container = OpenVoiceContainer()


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
        voice_chat_service = container.create_voice_chat_service(
            whisper_client=whisper_ai_client,
            falcon_client=falcon_ai_client,
        )
        response = voice_chat_service.generate(audio_path=file.file)
        return {"response": response}

    except Exception as e:
        logger.exception("Error in /chat/user_upload")
        raise HTTPException(
            status_code=500, detail=f"Error fetching response: {str(e)}"
        )
