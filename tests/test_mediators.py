from dataclasses import dataclass

import pytest

from pymediator import HandlerProtocolViolationException, InstanceRegistry, Mediator


class TestMediator:
    def test_send(self) -> None:
        @dataclass
        class SumRequest:
            x: int
            y: int

        class SumHandler:
            def handle(self, request: SumRequest) -> int:
                return request.x + request.y

        registry: InstanceRegistry = InstanceRegistry()
        registry.register(SumRequest, SumHandler)
        mediator: Mediator = Mediator(registry=registry)
        response: int = mediator.send(SumRequest(x=3, y=5))
        assert response == 8

    def test_send_with_invalid_handler_protocol(self) -> None:
        @dataclass
        class SumRequest:
            x: int
            y: int

        class SumHandler:
            def sum(self, request: SumRequest) -> int:
                return request.x + request.y

        registry: InstanceRegistry = InstanceRegistry()
        registry.register(SumRequest, SumHandler)
        mediator: Mediator = Mediator(registry=registry)
        with pytest.raises(HandlerProtocolViolationException):
            mediator.send(SumRequest(x=3, y=5))
