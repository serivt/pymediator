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

    def __init__(self, *, registry: Registry) -> None:
        self._registry: Registry = registry

    @abstractmethod
    def send(self, request: Request, dependencies: dict[str, Any] | None = None) -> Any:
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
    def send(self, request: Request, dependencies: dict[str, Any] | None = None) -> Any:
        handler: Handler = self._registry.get_handler(request)(**(dependencies or {}))
        if not isinstance(handler, Handler):
            raise HandlerProtocolViolationException(handler.__class__.__name__)
        return handler.handle(request)
