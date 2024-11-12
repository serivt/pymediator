from threading import Lock


class Singleton(type):
    """
    A thread-safe Singleton metaclass.

    This metaclass ensures that only one instance of a class exists throughout
    the program's execution. It uses a lock to synchronize threads during the
    first access to the Singleton, making the implementation thread-safe.

    Example:
        To create a Singleton class, define it with `SingletonMeta` as its metaclass:

        ```python
        class SingletonClass(metaclass=Singleton):
            value: str = None

            def __init__(self, value: str) -> None:
                self.value = value
        ```

        or

        ```python
        class SingletonClass(BaseClass):
            __metaclass__ = Singleton

        ```
    """

    _instances: dict["Singleton", "Singleton"] = {}
    _lock: Lock = Lock()

    def __call__(cls: "Singleton", *args: tuple, **kwargs: dict) -> "Singleton":
        """
        Creates or returns the single instance of the class.

        This thread-safe method checks if an instance of the class already exists.
        If not, it acquires a lock to prevent multiple threads from creating
        multiple instances concurrently. The lock is released once the instance
        is created.

        Args:
            *args (tuple): Positional arguments to pass to the class initializer.
            **kwargs (dict): Keyword arguments to pass to the class initializer.

        Returns:
            Singleton: The single instance of the class.
        """
        with cls._lock:
            if cls not in cls._instances:
                instance = super().__call__(*args, **kwargs)
                cls._instances[cls] = instance
        return cls._instances[cls]
