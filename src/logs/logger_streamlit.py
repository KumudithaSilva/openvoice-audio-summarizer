from typing import List
from interfaces.logging.i_ui_logging_interface import IUiLogger


class LoggerStreamlit(IUiLogger):
    """Logger for Streamlit UI."""

    def __init__(self):
        self.logs: List[str] = []

    def add(self, message: str) -> None:
        """Add a message to the log."""
        self.logs.append(message)

    def fetch(self) -> List[str]:
        """Return the list of logged messages."""
        return self.logs

    def empty(self) -> None:
        """
        Clear all messages from the logger.
        """
        self.logs.clear()
