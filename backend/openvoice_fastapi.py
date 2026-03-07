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
        logger.info("Starting FastAPI server: initializing AI client...")
        connection_service = container.create_chat_connection_service()
        app.state.ai_client = connection_service.connect()
        logger.info("AI client initialized successfully.")
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

        audio_service = container.create_audio_completion_service()
        audio_service.load_audio_file(file.file)

        audio_response = audio_service.preprocess_audio()
        audio = audio_response.waveform

        logger.debug(f"Response: {audio}")

        preview = audio[:, :100]

        if audio is None:
            raise RuntimeError("VoiceAI returned None")

        return {"response": preview.tolist()}

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

        ai_client = app.state.ai_client
        if ai_client is None:
            logger.error("AI client not initialized")
            raise RuntimeError("AI client not initialized")
        logger.info("AI client available for request")

        message_service = container.create_chat_messages()
        message = message_service.initialize(data.messages)

        completion_service = container.create_chat_completion_service(
            ai_client=ai_client
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
