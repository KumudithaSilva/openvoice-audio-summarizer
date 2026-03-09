from fastapi import Request
from logs.logger_singleton import Logger

logger = Logger(name="fastapi-dependencies")


def get_whisper_client(request: Request):
    client = request.app.state.whisper_ai_client
    if client is None:
        logger.error("WhisperAI client not initialized")
        raise RuntimeError("WhisperAI client not initialized")
    logger.info("WhisperAIclient available for request")
    return client


def get_falcon_client(request: Request):
    client = request.app.state.falcon_ai_client
    if client is None:
        logger.error("FalconAI client not initialized")
        raise RuntimeError("FalconAI client not initialized")
    logger.info("FalconAI client available for request")
    return client
