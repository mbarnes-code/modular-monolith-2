"""
Message Bus Factory

Factory for creating message bus adapter instances.
"""

import os
from typing import Any, Dict

import yaml

from .adapters import (EventBusAdapter, KafkaAdapter, RabbitMQAdapter,
                       SQSAdapter)
from .interfaces import ConfigurationError, IMessageBus, IMessageBusFactory


class MessageBusFactory(IMessageBusFactory):
    """
    Factory for creating message bus adapters.

    Supports config-driven adapter selection from:
    - YAML configuration files
    - Environment variables
    - Direct configuration dicts
    """

    # Adapter registry
    ADAPTERS = {
        "eventbus": EventBusAdapter,
        "rabbitmq": RabbitMQAdapter,
        "kafka": KafkaAdapter,
        "sqs": SQSAdapter,
    }

    @staticmethod
    def create(
        adapter_type: str = None,
        config: Dict[str, Any] = None,
    ) -> IMessageBus:
        """
        Create a message bus adapter instance.

        Args:
            adapter_type: Type of adapter (eventbus, rabbitmq, kafka, sqs)
                         If None, reads from MESSAGE_BUS_ADAPTER env var
            config: Adapter-specific configuration
                   If None, reads from MESSAGE_BUS_CONFIG env var (path to YAML)

        Returns:
            Configured message bus instance

        Raises:
            ValueError: If adapter_type is unknown
            ConfigurationError: If config is invalid

        Examples:
            # Create from direct config
            bus = MessageBusFactory.create(
                adapter_type="rabbitmq",
                config={"host": "localhost", "port": 5672}
            )

            # Create from environment variables
            # export MESSAGE_BUS_ADAPTER=eventbus
            # export MESSAGE_BUS_CONFIG=/path/to/config.yaml
            bus = MessageBusFactory.create()
        """
        # Determine adapter type
        if adapter_type is None:
            adapter_type = os.getenv("MESSAGE_BUS_ADAPTER", "eventbus")

        adapter_type = adapter_type.lower()

        if adapter_type not in MessageBusFactory.ADAPTERS:
            raise ValueError(
                f"Unknown adapter type: {adapter_type}. "
                f"Supported: {list(MessageBusFactory.ADAPTERS.keys())}"
            )

        # Load configuration
        if config is None:
            config = MessageBusFactory._load_config()

        # Validate configuration
        if not isinstance(config, dict):
            raise ConfigurationError(
                f"Configuration must be a dict, got {type(config)}"
            )

        # Create adapter instance
        adapter_class = MessageBusFactory.ADAPTERS[adapter_type]

        try:
            return adapter_class(config)
        except Exception as e:
            raise ConfigurationError(
                f"Failed to create {adapter_type} adapter: {e}"
            ) from e

    @staticmethod
    def create_from_yaml(yaml_path: str) -> IMessageBus:
        """
        Create adapter from YAML configuration file.

        YAML format:
        ```yaml
        adapter: rabbitmq
        config:
          host: localhost
          port: 5672
          username: guest
          password: guest
        ```

        Args:
            yaml_path: Path to YAML configuration file

        Returns:
            Configured message bus instance
        """
        try:
            with open(yaml_path, 'r') as f:
                data = yaml.safe_load(f)

            adapter_type = data.get("adapter")
            config = data.get("config", {})

            return MessageBusFactory.create(adapter_type, config)

        except FileNotFoundError:
            raise ConfigurationError(
                f"Configuration file not found: {yaml_path}")
        except yaml.YAMLError as e:
            raise ConfigurationError(f"Invalid YAML: {e}") from e

    @staticmethod
    def _load_config() -> Dict[str, Any]:
        """
        Load configuration from environment variables.

        Checks MESSAGE_BUS_CONFIG env var for path to YAML file.
        If not found, returns empty dict (adapter will use defaults).
        """
        config_path = os.getenv("MESSAGE_BUS_CONFIG")

        if config_path:
            try:
                with open(config_path, 'r') as f:
                    data = yaml.safe_load(f)
                    return data.get("config", {})
            except Exception as e:
                raise ConfigurationError(
                    f"Failed to load config from {config_path}: {e}"
                ) from e

        # Return empty config - adapters will use defaults
        return {}

    @staticmethod
    def get_available_adapters() -> list:
        """Get list of available adapter types"""
        return list(MessageBusFactory.ADAPTERS.keys())


# Convenience function for common use case
def create_message_bus(
    adapter_type: str = None,
    config: Dict[str, Any] = None,
) -> IMessageBus:
    """
    Convenience function to create message bus.

    Shorthand for MessageBusFactory.create()

    Args:
        adapter_type: Type of adapter (default: from env or "eventbus")
        config: Adapter configuration (default: from env or {})

    Returns:
        Configured message bus instance

    Example:
        ```python
        from libs.shared.messaging import create_message_bus, Message, Priority

        # Create bus (reads from env by default)
        bus = create_message_bus()

        await bus.start()

        # Publish message
        msg = Message(
            topic="security.threat.detected",
            payload={"ip": "192.168.1.100"},
            priority=Priority.HIGH,
        )

        await bus.publish(msg)
        ```
    """
    return MessageBusFactory.create(adapter_type, config)
