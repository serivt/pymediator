from abc import ABC, abstractmethod
from typing import Any

from pymediator.exceptions import HandlerProtocolViolationException
from pymediator.handlers import Handler, Request
from pymediator.registry import Registry


class BaseMediator(ABC):
    """
    Abstract base class for a mediator that handles sending requests to appropriate
    handlers.

    This class defines the contract for a mediator that interacts with a registry to
    obtain the correct handler for each request and delegates the task of handling the
    request to the handler.
    """

    def __init__(self, *, registry: Registry, dependencies: dict | None = None) -> None:
        self._registry: Registry = registry
        self._dependencies: dict = dependencies or {}

    @property
    def registry(self) -> Registry:
        return self._registry

    @abstractmethod
    def inject(self, **kwargs) -> "BaseMediator":  # type: ignore[no-untyped-def]
        """
        Abstract method to inject dependencies to the handler.

        Args:
            kwargs (dict[str, Any]): The dependencies to be injected.

        Returns:
            BaseMediator: A mediator instance ready to inject dependencies when making
                the handler call
        """

    @abstractmethod
    def send(self, request: Request) -> Any:
        """
        Abstract method to send the request to the handler.

        Args:
            request (Request): The request to be handled.
            dependencies (dict[str, Any] | None, optional): A dictionary of dependencies
                to pass to the handler during execution.

        Returns:
            Any: The result from handling the request.
        """


class Mediator(BaseMediator):
    def inject(self, **kwargs) -> "Mediator":  # type: ignore[no-untyped-def]
        return Mediator(registry=self.registry, dependencies=kwargs)

    def send(self, request: Request) -> Any:
        handler: Handler = self._registry.get_handler(request)(**self._dependencies)
        if not isinstance(handler, Handler):
            raise HandlerProtocolViolationException(handler.__class__.__name__)
        return handler.handle(request)
