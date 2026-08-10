from __future__ import annotations
from math import comb


def tail(n: int, k: int, p: float) -> float:
    return sum(comb(n, i) * p**i * (1 - p) ** (n - i) for i in range(k, n + 1))


def main() -> None:
    n = 36
    critical = min(k for k in range(n + 1) if tail(n, k, 0.5) <= 0.025)
    power = tail(n, critical, 0.75)
    print(f"paired directional design: n={n}, two-sided alpha≈0.05, critical={critical}/{n}, power at p=0.75={power:.3f}")


if __name__ == "__main__":
    main()
