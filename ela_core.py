#!/usr/bin/env python3
"""
ELA core — Executable Logic for Arithmetic Descent Certificates.

Boundary:
This program does not prove the Collatz conjecture.

It generates and verifies finite local descent certificates for the
accelerated odd Collatz/Syracuse map:

    T(n) = (3n + 1) / 2^v2(3n + 1)

The purpose is exact integer replay, reproducible telemetry,
and finite-block descent verification.
"""

from __future__ import annotations

import argparse
import json
from math import log2
from typing import Any, Dict, List


VALID_STATUSES = {"certified", "terminal", "open_in_limit"}


def v2(m: int) -> int:
    """
    Return the exponent of 2 dividing a positive integer m.
    """
    if not isinstance(m, int) or m <= 0:
        raise ValueError("v2 expects a positive integer")

    return (m & -m).bit_length() - 1


def validate_start(n: int) -> None:
    """
    Validate that n is a positive odd integer for the accelerated odd map.
    """
    if not isinstance(n, int):
        raise TypeError("n must be an integer")

    if n <= 0:
        raise ValueError("n must be positive")

    if n % 2 == 0:
        raise ValueError(
            "n must be odd for the accelerated odd map. "
            "For an even input, divide by powers of 2 first."
        )


def step(n: int) -> Dict[str, Any]:
    """
    Perform one accelerated odd Collatz/Syracuse step.

    Returns exact integer values and floating telemetry:

        m = 3n + 1
        valuation = v2(m)
        next_n = m / 2^valuation

    The logarithmic balance identity is:

        log2(T(n) / n) = log2(3 + 1/n) - v2(3n + 1)

    Therefore the local descent contribution is:

        balance_delta = v2(3n + 1) - log2(3 + 1/n)
    """
    validate_start(n)

    m = 3 * n + 1
    valuation = v2(m)
    next_n = m >> valuation

    growth_cost = log2(3 + (1 / n))
    balance_delta = valuation - growth_cost

    return {
        "n": n,
        "m": m,
        "v2": valuation,
        "next_n": next_n,
        "growth_cost": growth_cost,
        "balance_delta": balance_delta,
    }


def generate_certificate(n0: int, max_steps: int = 10000) -> Dict[str, Any]:
    """
    Generate a finite descent certificate attempt.

    A certificate is marked "certified" when the accelerated odd orbit
    reaches a value below the starting value n0:

        T^k(n0) < n0

    It is marked "terminal" only for n0 = 1.

    It is marked "open_in_limit" when no descent below n0 is found
    within max_steps.
    """
    validate_start(n0)

    if max_steps <= 0:
        raise ValueError("max_steps must be positive")

    if n0 == 1:
        return {
            "n0": n0,
            "status": "terminal",
            "max_steps": max_steps,
            "steps": 0,
            "descent_step": None,
            "final_n": 1,
            "cumulative_balance": 0.0,
            "trace": [],
        }

    current = n0
    cumulative_balance = 0.0
    trace: List[Dict[str, Any]] = []

    for j in range(max_steps):
        row = step(current)
        cumulative_balance += row["balance_delta"]

        row["j"] = j
        row["cumulative_balance"] = cumulative_balance

        trace.append(row)

        if row["next_n"] < n0:
            return {
                "n0": n0,
                "status": "certified",
                "max_steps": max_steps,
                "steps": j + 1,
                "descent_step": j + 1,
                "final_n": row["next_n"],
                "cumulative_balance": cumulative_balance,
                "trace": trace,
            }

        current = row["next_n"]

    return {
        "n0": n0,
        "status": "open_in_limit",
        "max_steps": max_steps,
        "steps": max_steps,
        "descent_step": None,
        "final_n": current,
        "cumulative_balance": cumulative_balance,
        "trace": trace,
    }


def verify_certificate(cert: Dict[str, Any]) -> bool:
    """
    Strictly verify a generated ELA certificate by exact integer replay.

    This function does not prove anything globally.
    It only checks whether the supplied finite certificate is internally valid.
    """
    if not isinstance(cert, dict):
        return False

    n0 = cert.get("n0")
    status = cert.get("status")
    trace = cert.get("trace")

    if status not in VALID_STATUSES:
        return False

    if not isinstance(trace, list):
        return False

    try:
        validate_start(n0)
    except Exception:
        return False

    if status == "terminal":
        return n0 == 1 and len(trace) == 0 and cert.get("final_n") == 1

    current = n0
    cumulative_balance = 0.0
    found_descent = False

    for j, stored in enumerate(trace):
        try:
            replay = step(current)
        except Exception:
            return False

        cumulative_balance += replay["balance_delta"]

        if stored.get("j") != j:
            return False

        if stored.get("n") != replay["n"]:
            return False

        if stored.get("m") != replay["m"]:
            return False

        if stored.get("v2") != replay["v2"]:
            return False

        if stored.get("next_n") != replay["next_n"]:
            return False

        if replay["next_n"] < n0:
            found_descent = True

        current = replay["next_n"]

    if status == "certified":
        if not trace:
            return False

        return (
            found_descent
            and cert.get("final_n") == trace[-1].get("next_n")
            and cert.get("descent_step") == cert.get("steps")
        )

    if status == "open_in_limit":
        return not found_descent

    return False


def main() -> None:
    parser = argparse.ArgumentParser(
        description="ELA finite descent certificate generator"
    )
    parser.add_argument(
        "numbers",
        nargs="*",
        type=int,
        default=[7, 27, 97, 871, 6171, 77031],
        help="positive odd integers to test",
    )
    parser.add_argument(
        "--max-steps",
        type=int,
        default=10000,
        help="maximum accelerated odd steps",
    )
    parser.add_argument(
        "--no-trace",
        action="store_true",
        help="omit full trace from JSON output",
    )

    args = parser.parse_args()

    results = []

    for n in args.numbers:
        cert = generate_certificate(n, max_steps=args.max_steps)
        cert["verified"] = verify_certificate(cert)

        if args.no_trace:
            cert = dict(cert)
            cert["trace"] = []

        results.append(cert)

    if len(results) == 1:
        print(json.dumps(results[0], indent=2, ensure_ascii=False))
    else:
        print(json.dumps(results, indent=2, ensure_ascii=False))


if __name__ == "__main__":
    main()
