"""Tiny helpers so the tests are plain asserts (no print-based checks)."""

import math
from typing import Callable, Type


def approx(a: float, b: float, tol: float = 1e-6) -> bool:
    """True if ``a`` and ``b`` agree within ``tol``."""
    return math.isclose(a, b, abs_tol=tol)


def raises(exc: Type[BaseException], fn: Callable, *args, **kwargs) -> bool:
    """True if ``fn(*args, **kwargs)`` raises ``exc``."""
    try:
        fn(*args, **kwargs)
    except exc:
        return True
    return False
