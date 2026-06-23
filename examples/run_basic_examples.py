#!/usr/bin/env python3
"""
Basic ELA examples.

This script runs the ELA finite descent certificate engine
on a small set of known odd inputs.
"""

from ela_core import generate_certificate, verify_certificate


def main():
    numbers = [7, 27, 97, 871, 6171, 77031]

    for n in numbers:
        cert = generate_certificate(n, max_steps=10000)
        verified = verify_certificate(cert)

        print("=" * 60)
        print(f"n0: {n}")
        print(f"status: {cert['status']}")
        print(f"steps: {cert['steps']}")
        print(f"final_n: {cert['final_n']}")
        print(f"descent_step: {cert['descent_step']}")
        print(f"cumulative_balance: {cert['cumulative_balance']}")
        print(f"verified: {verified}")


if __name__ == "__main__":
    main()
