from contextlib import asynccontextmanager

import uvicorn
from fastapi import FastAPI, File, HTTPException, UploadFile
from pydantic import BaseModel

from container.openvoice_container import OpenVoiceContainer
from logs.logger_singleton import Logger

logger = Logger(name="fastapi")
container = OpenVoiceContainer()


# --- FastAPI app with lifespan context manager ---
@asynccontextmanager
async def lifespan(app: FastAPI):
    """
    Initializes the AI client at startup.
    """
    try:
        # logger.info("Starting FastAPI server: initializing FalconAI client...")
        # falcon_connection_service = container.create_chat_connection_service()
        # app.state.falcon_ai_client = falcon_connection_service.connect()
        # logger.info("FalconAI client initialized successfully.")

        logger.info("Starting WhisperAPI server: initializing WhisperAPI client...")
        whisper_connection_service = container.create_voice_connection_service()
        app.state.whisper_ai_client = whisper_connection_service.connect()
        logger.info("WhisperAPI client initialized successfully.")

        yield

    except Exception:
        logger.exception("Error during FastAPI startup")
        raise
    finally:
        logger.info("FastAPI server shutting down...")


app = FastAPI(title="Falcon 3 OpenVoice Audio Summarizer API", lifespan=lifespan)


# --- Pydantic models ---
class ChatResponse(BaseModel):
    """
    Response model for initial chat history.
    """

    messages: str


# --- Routes ---
@app.post("/chat/user_upload")
async def user_upload(file: UploadFile = File(...)):
    """
    Handle audio file upload and return AI response.
    """
    logger.info("Received request to /chat/user_upload")
    try:
        # bytes of audio file
        logger.debug(f"File received: {file.filename}, type: {file.content_type}")

        whisper_ai_client = app.state.whisper_ai_client
        if whisper_ai_client is None:
            logger.error("WhisperAI client not initialized")
            raise RuntimeError("WhisperAI client not initialized")
        logger.info("WhisperAIclient available for request")

        audio_service = container.create_transcription_completion_service(
            ai_client=whisper_ai_client
        )
        response = audio_service.generate(audio_path=file.file)
        logger.debug(f"Response: {response}")

        if response is None:
            raise RuntimeError("WhisperAI returned None")

        return {"response": response}

    except Exception as e:
        logger.exception("Error in /chat/user_upload")
        raise HTTPException(
            status_code=500, detail=f"Error fetching response: {str(e)}"
        )


@app.post("/chat/send_request")
def user_request(data: ChatResponse):
    """
    Handle chat request from user and return AI response.
    """
    logger.info("Received request to /chat/send_request")
    try:
        logger.debug(f"Incoming messages: {data.messages}")

        falcon_ai_client = app.state.falcon_ai_client
        if falcon_ai_client is None:
            logger.error("FalconAI client not initialized")
            raise RuntimeError("FalconAI client not initialized")
        logger.info("FalconAI client available for request")

        message_service = container.create_chat_messages()
        message = message_service.initialize(data.messages)

        completion_service = container.create_chat_generation_service(
            ai_client=falcon_ai_client
        )
        response = completion_service.generate(messages=message)

        logger.debug(f"Response: {response}")
        if response is None:
            raise RuntimeError("FalconAI returned None")

        return {"response": response}

    except Exception as e:
        logger.exception("Error in /chat/send_request")
        raise HTTPException(
            status_code=500, detail=f"Error fetching response: {str(e)}"
        )


# --- Run Uvicorn ---
if __name__ == "__main__":
    uvicorn.run(host="127.0.0.1", port=8000, app="openvoice_fastapi:app", reload=True)
