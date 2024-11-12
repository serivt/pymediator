from typing import Any, Protocol, runtime_checkable

from pymediator.exceptions import ProtocolInheritanceException


@runtime_checkable
class Request(Protocol):
    def __init_subclass__(cls) -> None:
        raise ProtocolInheritanceException()


@runtime_checkable
class Handler(Protocol):
    def __init_subclass__(cls) -> None:
        raise ProtocolInheritanceException()

    def handle(self, request: Any) -> Any:
        raise NotImplementedError()
