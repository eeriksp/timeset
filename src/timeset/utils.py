from typing import Type, Any


def ensure(condition: Any, exception_cls: Type[Exception], msg: str):
    if not condition:
        raise exception_cls(msg)


def preclude(condition: Any, exception_cls: Type[Exception], msg: str):
    ensure(not condition, exception_cls, msg)
