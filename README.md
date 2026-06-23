# ELA — Executable Logic for Arithmetic Descent Certificates

ELA is a minimal executable framework for generating and verifying finite descent certificates for the accelerated odd Collatz/Syracuse map.

## Boundary

This repository does not claim to prove the Collatz conjecture.

It provides reproducible computational artifacts, exact integer replay, and finite-block descent certificate verification.

## Core Map

For odd positive integers, the accelerated map is:

T(n) = (3n + 1) / 2^v₂(3n + 1)

The local balance identity is:

log₂(T(n) / n) = log₂(3 + 1/n) - v₂(3n + 1)

A finite block certifies descent when:

B(n₀, k) = Σ [v₂(3Tʲ(n₀)+1) - log₂(3 + 1/Tʲ(n₀))] > 0

which is equivalent to:

Tᵏ(n₀) < n₀

## What this is

ELA is a finite verification architecture.

It checks whether a given input produces a local descent certificate under exact integer replay.

## What this is not

ELA is not a complete proof of the Collatz conjecture.

It does not claim a universal bound for all integers.

It does not replace formal proof.

## Citation

Please cite the Zenodo DOI when referencing this work:

DOI: 10.5281/zenodo.20785851

## Paper

The accompanying technical paper is available here:

[ELA Verifiable Certificate Engine v1.3.1](./ELA_Verifiable_Certificate_Engine_for_Collatz_Type_Descent_Tracing_v1_3_1.pdf)

## How to Run

Run the core engine with default benchmark inputs:

```bash
python ela_core.py
