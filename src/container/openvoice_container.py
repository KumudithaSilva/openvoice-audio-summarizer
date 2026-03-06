from components.chat_completion import ChatCompletionService
from components.chat_connection import ChatConnectionService
from components.chat_messages import MessageCompletionService
from infrastructure.falcon_prompt import PromptProvider
from infrastructure.falconai_service import FalconAIService
from interfaces.chat.i_chat_history import IMessageCompletionService
from interfaces.chat.i_oneshot_prompt import IPrompt
from interfaces.chat.i_voice_complete import IVoiceCompletionService
from interfaces.chat.i_voice_connection import IVoiceConnection
from interfaces.infra.i_config_provider import IConfigProvider
from infrastructure.config_provider import ConfigProvider
from interfaces.llm.i_ai_client import IAIClient
from interfaces.llm.i_falcon_operations import IFalconAIOperations


class OpenVoiceContainer:
    """
    Factory to wire all dependencies and return orchestrator service instances.
    """

    def create_chat_connection_service(
        self,
        config_provider: IConfigProvider = None,
    ) -> IVoiceConnection:
        """
        Create and return a llm connection service with concrete
        or default dependencies.
        """
        if config_provider is None:
            config_provider = ConfigProvider()

        return ChatConnectionService(config_provider)

    def create_chat_messages(self) -> IMessageCompletionService:
        """
        Create and return a chat completion service.
        """
        prompt_provider: IPrompt = PromptProvider()
        return MessageCompletionService(prompt_provider)

    def create_chat_completion_service(
        self,
        ai_client: IAIClient,
    ) -> IVoiceCompletionService:
        """
        Create and return a chat completion service using the
        provided AI client.
        """
        falcon_service: IFalconAIOperations = FalconAIService(ai_client)
        return ChatCompletionService(falcon_service)
