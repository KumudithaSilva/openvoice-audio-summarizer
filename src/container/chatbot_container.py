from components.chat_connection import ChatConnectionService
from interfaces.chat.i_chatbot_connection import IChatConnection
from interfaces.infra.i_config_provider import IConfigProvider
from infrastructure.config_provider import ConfigProvider


class ChatbotContainer:
    """
    Factory to wire all dependencies and return orchestrator service instances.
    """

    def create_chat_connection_service(
        self,
        config_provider: IConfigProvider = None,
    ) -> IChatConnection:
        """
        Create and return a chat connection service with concrete
        or default dependencies.
        """
        if config_provider is None:
            config_provider = ConfigProvider()

        return ChatConnectionService(config_provider)
