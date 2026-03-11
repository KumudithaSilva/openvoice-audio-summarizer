import os

from logs.logger_singleton import Logger
from interfaces.infra.i_config_provider import IConfigProvider
import yaml
from typing import Optional


class ConfigProvider(IConfigProvider):
    """
    Provider for Falcon model details, loading from a YAML config.
    """

    def __init__(self, config_path: str = "config.yaml", logger=None):
        """
        Initialize the ConfigProvider instance.

        Args:
            config_path (str): Path to the YAML config file.
            logger (Logger, optional): Logger instance. If None, a default is used.
        """
        self.config_path = config_path
        self.logger = logger or Logger(self.__class__.__name__)
        self._config_data = self._load_config()

    def _load_config(self) -> dict:
        """
        Load YAML configuration file into a dictionary.
        """
        try:
            with open(self.config_path, "r") as f:
                data = yaml.safe_load(f)
            self.logger.info(f"Loaded config from {self.config_path}")
            return data
        except Exception as e:
            self.logger.error(f"Failed to load config: {e}")
            return {}

    def get_model_details(
        self, model_name: str = "Falcon3-1B-Instruct"
    ) -> Optional[str]:
        """
        Get the specified model details.

        Args:
            model_name (str): The name of the model.

        Returns:
            str | None: Details of the model if found, else None.
        """
        details = self._config_data.get("models", {}).get(model_name)
        if details:
            self.logger.info(f"Model '{model_name}' found in config")
        else:
            self.logger.warning(f"Model '{model_name}' not found in config")
        return details


if __name__ == "__main__":
    cp = ConfigProvider()
    print(cp.get_model_details())
