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

    def test_injection(self) -> None:
        class SumUtils:
            def sum(self, x: int, y: int) -> int:
                return x + y

        @dataclass
        class SumRequest:
            x: int
            y: int

        class SumHandler:
            def __init__(self, sum_utils: SumUtils) -> None:
                self._sum_utils: SumUtils = sum_utils

            def handle(self, request: SumRequest) -> int:
                return self._sum_utils.sum(request.x, request.y)

        registry: InstanceRegistry = InstanceRegistry()
        registry.register(SumRequest, SumHandler)
        mediator: Mediator = Mediator(registry=registry)
        response: int = mediator.inject(sum_utils=SumUtils()).send(SumRequest(x=3, y=5))
        assert response == 8

    def test_injection_multiple(self) -> None:
        class SumUtils:
            def sum(self, x: int, y: int) -> int:
                return x + y

        class MultiplyUtils:
            def multiply(self, x: int, y: int) -> int:
                return x * y

        @dataclass
        class SumRequest:
            x: int
            y: int

        class SumHandler:
            def __init__(self, sum_utils: SumUtils) -> None:
                self._sum_utils: SumUtils = sum_utils

            def handle(self, request: SumRequest) -> int:
                return self._sum_utils.sum(request.x, request.y)

        @dataclass
        class MultiplyRequest:
            x: int
            y: int

        class MultiplyHandler:
            def __init__(self, multiply_utils: MultiplyUtils) -> None:
                self._multiply_utils: MultiplyUtils = multiply_utils

            def handle(self, request: MultiplyRequest) -> int:
                return self._multiply_utils.multiply(request.x, request.y)

        registry: InstanceRegistry = InstanceRegistry()
        registry.register(SumRequest, SumHandler)
        registry.register(MultiplyRequest, MultiplyHandler)
        mediator: Mediator = Mediator(registry=registry).inject(
            sum_utils=SumUtils(), multiply_utils=MultiplyUtils()
        )
        assert mediator.send(SumRequest(x=3, y=5)) == 8
        assert mediator.send(MultiplyRequest(x=3, y=5)) == 15
