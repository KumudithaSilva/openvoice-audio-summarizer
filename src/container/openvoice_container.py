from components.chat_connection import ChatConnectionService
from interfaces.chat.i_voice_connection import IVoiceConnection
from interfaces.infra.i_config_provider import IConfigProvider
from infrastructure.config_provider import ConfigProvider


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
