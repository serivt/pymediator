# Pymediator

Provides a lightweight and extensible implementation of the Mediator pattern in Python, specifically designed for systems that follow the CQRS (Command Query Responsibility Segregation) pattern. Its architecture allows for a clear separation of command and query logic, making it ideal for clean architectures and event-driven systems.

## Install
```bash
pip install pymediator
```

# Usage
```python
from dataclases import dataclass
from pymediator import Mediator as _Mediator, SingletonRegistry

registry: SingletonRegistry = SingletonRegistry()

@dataclass
class SumRequest:
    x: int | float
    y: int | float

class SumHandler:
    def handle(self, request: SumRequest) -> int | float:
        return request.x + request.y

registry.register(SumRequest, SumHandler)

class Mediator(_Mediator):
    def __init__(self) -> None:
        super().__init__(registry=SingletonRegistry())

mediator: Mediator = Mediator()

mediator.send(SumRequest(x=3, y=8)) # Output: 11
```

## Recommended use
```python
# my_app/application/queries/sum.py
from dataclases import dataclass

@dataclass
class SumRequest:
    x: int | float
    y: int | float

class SumHandler:
    def handle(self, request: SumRequest) -> int | float:
        return request.x + request.y
```

```python
# my_app/infrastructure/mediator.py
from pymediator import SingletonRegistry
from my_app.application.queries.sum import SumRequest, SumHandler

registry: SingletonRegistry = SingletonRegistry()

registry.register(SumRequest, SumHandler)
```

```python
# my_app/infrastructure/console.py
import sys
from my_app.application.queries.sum import SumRequest

@inject
def main(x: int, y: int, mediator: Mediator = Provide[AppContainer.mediator]) -> None:
    print(mediator.send(SumRequest(x=x, y=y)))

if __name__ == "__main__":
    num1: int = int(sys.argv[1])
    num2: int = int(sys.argv[2])
    main(num1, num2)
```
