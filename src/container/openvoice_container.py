from components.chat_generation import ChatGenerationService
from components.chat_connection import ChatConnectionService
from components.chat_messages import MessageCompletionService
from components.voice_connection import VoiceConnectionService
from components.voice_transcription import VoiceTranscriptionService
from infrastructure.audio_processor import AudioProcessor
from infrastructure.falcon_prompt import PromptProvider
from infrastructure.falconai_service import FalconAIService
from infrastructure.whisper_service import WhisperAIService
from interfaces.audio.i_audio_processor import IAudioProcessor
from interfaces.chat.i_chat_history import IMessageCompletionService
from interfaces.chat.i_oneshot_prompt import IPrompt
from interfaces.chat.i_text_generation import ITextGenereateService
from interfaces.chat.i_falcon_connection import IFalconConnection
from interfaces.chat.i_voice_transcription import IVoiceTranscriptionService
from interfaces.chat.i_whisper_connection import IWhisperConnection
from interfaces.infra.i_config_provider import IConfigProvider
from infrastructure.config_provider import ConfigProvider
from interfaces.llm.i_ai_client import IAIClient
from interfaces.llm.i_falcon_operations import IFalconAIOperations
from interfaces.llm.i_voice_ai_client import IWhisperClient
from interfaces.llm.i_whisper_operations import IWhisperOperations


class OpenVoiceContainer:
    """
    Factory to wire all dependencies and return orchestrator service instances.
    This container provides methods to create services for FalconAI and WhisperAI.
    """

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

    def create_chat_messages(self) -> IMessageCompletionService:
        """
        Create and return a Falcon chat completion service
        with a default prompt provider.
        """
        prompt_provider: IPrompt = PromptProvider()
        return MessageCompletionService(prompt_provider)

    def create_chat_generation_service(
        self,
        ai_client: IAIClient,
    ) -> ITextGenereateService:
        """
        Create and return a chat generation service using the
        provided Falcon AI client.
        """
        falcon_service: IFalconAIOperations = FalconAIService(ai_client)
        return ChatGenerationService(falcon_service)

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
        whisper_service: IWhisperOperations = WhisperAIService(ai_client)
        audio_processor: IAudioProcessor = AudioProcessor()

        return VoiceTranscriptionService(whisper_service, audio_processor)
