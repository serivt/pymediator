import pytest

from pymediator.exceptions import ProtocolInheritanceException
from pymediator.handlers import Handler, Request


class TestRequest:
    def test_prohibit_subclassing(self) -> None:
        with pytest.raises(ProtocolInheritanceException):

            class RequestTest(Request):
                pass


class TestHandler:
    def test_prohibit_subclassing(self) -> None:
        with pytest.raises(ProtocolInheritanceException):

            class HandlerTest(Handler):
                pass
