class ProtocolInheritanceException(Exception):
    def __init__(self) -> None:
        super().__init__("Protocols cannot be inherited.")


class HandlerProtocolViolationException(Exception):
    def __init__(self, class_name: str) -> None:
        super().__init__(
            f"The class '{class_name}' does not conform to the expected Handler Protocol."
        )
        self.class_name = class_name


class RequestAlreadyRegisteredException(Exception):
    def __init__(self) -> None:
        super().__init__("The handler is already registered.")


class HandlerNotFoundException(Exception):
    def __init__(self) -> None:
        super().__init__("Handler not found")
