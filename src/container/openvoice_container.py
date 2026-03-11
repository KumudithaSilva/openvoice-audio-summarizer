from components.chat_generation import ChatGenerationService
from components.chat_connection import ChatConnectionService
from components.voice_chat_generation import VoiceChatService
from components.voice_connection import VoiceConnectionService
from components.voice_transcription import VoiceTranscriptionService
from infrastructure.audio_processor import AudioProcessor
from infrastructure.falcon_prompt import PromptProvider
from infrastructure.falconai_service import FalconAIService
from infrastructure.whisper_service import WhisperAIService
from interfaces.audio.i_audio_processor import IAudioProcessor
from interfaces.chat.i_oneshot_prompt import IPrompt
from interfaces.chat.i_text_generation import ITextGenereateService
from interfaces.chat.i_falcon_connection import IFalconConnection
from interfaces.chat.i_voice_chat import IVoiceChatService
from interfaces.chat.i_voice_transcription import IVoiceTranscriptionService
from interfaces.chat.i_whisper_connection import IWhisperConnection
from interfaces.infra.i_config_provider import IConfigProvider
from infrastructure.config_provider import ConfigProvider
from interfaces.llm.i_ai_client import IAIClient
from interfaces.llm.i_falcon_operations import IFalconAIOperations
from interfaces.llm.i_voice_ai_client import IWhisperClient
from interfaces.llm.i_whisper_operations import IWhisperOperations
from interfaces.logging.i_ui_logging_interface import IUiLogger
from logs.logger_streamlit import LoggerStreamlit


class OpenVoiceContainer:
    """
    Factory to wire all dependencies and return orchestrator service instances.
    This container provides methods to create services for FalconAI and WhisperAI.
    """

    def __init__(self):
        # Shared Streamlit logger for all services
        self._streamlit_logger: LoggerStreamlit = LoggerStreamlit()

    #### Falcon Services ####

    def create_chat_connection_service(
        self,
        config_provider: IConfigProvider | None = None,
    ) -> IFalconConnection:
        """
        Create and return a Falcon LLM connection service with
        either the provided config provider or a default one.
        """
        if config_provider is None:
            config_provider = ConfigProvider()

        return ChatConnectionService(config_provider)

    def create_chat_generation_service(
        self,
        ai_client: IAIClient,
        prompt_provider: IPrompt | None = None,
    ) -> ITextGenereateService:
        """
        Create and return a chat generation service using the
        provided Falcon AI client and prompt provider.
        """
        falcon_service: IFalconAIOperations = FalconAIService(
            ai_client, logger_streamlit=self._streamlit_logger
        )

        if prompt_provider is None:
            prompt_provider = PromptProvider()

        return ChatGenerationService(falcon_service, prompt_provider)

    #### Whisper Services ####

    def create_voice_connection_service(
        self,
        config_provider: IConfigProvider | None = None,
    ) -> IWhisperConnection:
        """
        Create and return a Whisper LLM connection service with
        either the provided config provider or a default one.
        """
        if config_provider is None:
            config_provider = ConfigProvider()

        return VoiceConnectionService(config_provider)

    def create_transcription_completion_service(
        self,
        ai_client: IWhisperClient,
    ) -> IVoiceTranscriptionService:
        """
        Create and return an audio transcription service using the
        provided Whisper AI client and Audio preprocessor.
        """
        whisper_service: IWhisperOperations = WhisperAIService(
            ai_client, logger_streamlit=self._streamlit_logger
        )
        audio_processor: IAudioProcessor = AudioProcessor(
            logger_streamlit=self._streamlit_logger
        )

        return VoiceTranscriptionService(whisper_service, audio_processor)

    #### Falcon and Whisper Services ####

    def create_voice_chat_service(
        self,
        whisper_client: IWhisperClient,
        falcon_client: IAIClient,
        prompt_provider: IPrompt | None = None,
    ) -> IVoiceChatService:
        """
        Create combination of audio transcription service and Falcon AI
        client text genration service and return generated response.
        """

        transcription_service = self.create_transcription_completion_service(
            ai_client=whisper_client
        )
        chat_service = self.create_chat_generation_service(
            ai_client=falcon_client,
            prompt_provider=prompt_provider,
        )

        return VoiceChatService(
            transcription_service=transcription_service,
            chat_service=chat_service,
        )

    #### Falcon and Whisper Streamlit Log Services ####

    def streamlit_logs(self) -> IUiLogger:
        """
        Create streamlit logging services for audio transcription service and Falcon AI
        text genration.
        """
        return self._streamlit_logger
