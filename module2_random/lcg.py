"""Linear congruential generator: X(n+1) = (a X(n) + c) mod m."""

from typing import List


class LinearCongruentialGenerator:
    """Reproducible LCG producing uniforms U = X/m in [0, 1).

    Args:
        seed: Initial state X(0).
        a: Multiplier (default 1103515245).
        c: Increment (default 12345).
        m: Modulus (default 2**31).

    Example:
        >>> g = LinearCongruentialGenerator(seed=1)
        >>> 0 <= g.next() < 1
        True
    """

    def __init__(self, seed: int = 12345, a: int = 1103515245,
                 c: int = 12345, m: int = 2 ** 31) -> None:
        if m <= 0:
            raise ValueError("m must be positive")
        self.a, self.c, self.m = a, c, m
        self.state = seed % m

    def next(self) -> float:
        """Advance the state and return U in [0, 1)."""
        self.state = (self.a * self.state + self.c) % self.m
        return self.state / self.m

    def generate(self, n: int) -> List[float]:
        """Return ``n`` successive values."""
        return [self.next() for _ in range(n)]

    def next_digit(self) -> int:
        """Two-digit random number 0-99."""
        return int(self.next() * 100)
