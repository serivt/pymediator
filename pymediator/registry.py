from abc import ABC, abstractmethod
from typing import Type

from pymediator.exceptions import (
    HandlerNotFoundException,
    RequestAlreadyRegisteredException,
)
from pymediator.handlers import Handler, Request
from pymediator.utils import Singleton


class Registry(ABC):
    """
    Abstract base class for a registry that handles the registration and
    retrieval of request-handler pairs.

    This class provides an interface for managing handlers associated with
    specific request types, supporting operations for registering, retrieving,
    and clearing handlers in the registry.
    """

    @abstractmethod
    def register(self, request: Type[Request], handler: Type[Handler]) -> None:
        """
        Registers a handler for a given request type.

        Args:
            request (Type[Request]): The request type to associate with the handler.
            handler (Type[Handler]): The handler to register for the request type.
        """

    @abstractmethod
    def get_handler(self, request: Request) -> Type[Handler]:
        """
        Retrieves the handler associated with a given request.

        Args:
            request (Request): The request instance for which to retrieve the handler.

        Returns:
            Type[Handler]: The handler associated with the specified request type.
        """

    @abstractmethod
    def clear(self) -> None:
        """
        Clears all registered handlers in the registry.

        This method removes all request-handler associations, resetting the registry
        to an empty state.
        """


class InstanceRegistry(Registry):
    def __init__(self) -> None:
        self._handlers: dict[Type[Request], Type[Handler]] = {}

    def register(self, request: Type[Request], handler: Type[Handler]) -> None:
        if request in self._handlers:
            raise RequestAlreadyRegisteredException()
        self._handlers[request] = handler

    def get_handler(self, request: Request) -> Type[Handler]:
        handler: Type[Handler] | None = self._handlers.get(type(request))
        if handler is None:
            raise HandlerNotFoundException()
        return handler

    def clear(self) -> None:
        self._handlers = {}


class _SingletonRegistryMeta(type(InstanceRegistry), Singleton): ...  # type: ignore[misc]


class SingletonRegistry(InstanceRegistry, metaclass=_SingletonRegistryMeta):  # type: ignore[misc]
    pass
