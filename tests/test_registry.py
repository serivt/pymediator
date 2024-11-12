from typing import Type

import pytest

from pymediator import (
    Handler,
    HandlerNotFoundException,
    RequestAlreadyRegisteredException,
    SingletonRegistry,
)


class RequestTest:
    pass


class HandlerTest:
    def handle(self, request: RequestTest) -> int:
        return 0


class TestLocalRegistry:
    @pytest.fixture
    def registry(self) -> SingletonRegistry:
        registry: SingletonRegistry = SingletonRegistry()
        registry.clear()
        return registry

    def test_register(self, registry: SingletonRegistry) -> None:
        registry.register(RequestTest, HandlerTest)
        assert len(registry._handlers) == 1

    def test_register_already_registered_request(
        self, registry: SingletonRegistry
    ) -> None:
        registry.register(RequestTest, HandlerTest)
        with pytest.raises(RequestAlreadyRegisteredException):
            registry.register(RequestTest, HandlerTest)

    def test_get_handler(self, registry: SingletonRegistry) -> None:
        registry.register(RequestTest, HandlerTest)
        handler: Type[Handler] = registry.get_handler(RequestTest())
        assert handler is HandlerTest

    def test_get_handler_not_found(self, registry: SingletonRegistry) -> None:
        with pytest.raises(HandlerNotFoundException):
            registry.get_handler(RequestTest())

    def test_singleton_behavior(self, registry: SingletonRegistry) -> None:
        registry.register(RequestTest, HandlerTest)
        handler: Type[Handler] = SingletonRegistry().get_handler(RequestTest())
        assert handler is HandlerTest
