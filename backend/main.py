from contextlib import asynccontextmanager
from fastapi import FastAPI
from container.openvoice_container import OpenVoiceContainer
from logs.logger_singleton import Logger
from routes import chat
import uvicorn

logger = Logger(name="fastapi")
container = OpenVoiceContainer()


# --- FastAPI app with lifespan context manager ---
@asynccontextmanager
async def lifespan(app: FastAPI):
    """
    Initializes the AI client at startup.
    """
    try:
        logger.info("Starting FastAPI server: initializing FalconAI client...")
        falcon_connection_service = container.create_chat_connection_service()
        app.state.falcon_ai_client = falcon_connection_service.connect()
        logger.info("FalconAI client initialized successfully.")

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
app.include_router(chat.router)


# --- Run Uvicorn ---
if __name__ == "__main__":
    uvicorn.run(host="127.0.0.1", port=8000, app="main:app", reload=True)
