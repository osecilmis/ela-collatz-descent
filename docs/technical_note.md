# Technical Note

## ELA — Executable Logic for Arithmetic Descent Certificates

ELA is a finite-block verification framework for the accelerated odd Collatz/Syracuse map.

The accelerated odd map is:

T(n) = (3n + 1) / 2^v₂(3n + 1)

for positive odd integers.

## Purpose

The purpose of ELA is to generate and verify finite local descent certificates.

A descent certificate is produced when an orbit starting at n₀ reaches a later odd value below n₀:

Tᵏ(n₀) < n₀

This is a local, finite, replayable certificate.

## Boundary

ELA does not claim to prove the Collatz conjecture.

It does not establish a universal bound for all positive integers.

It does not replace formal mathematical proof.

Instead, it provides an executable verification architecture based on exact integer replay.

## Local Balance Identity

For one accelerated step:

T(n) = (3n + 1) / 2^v₂(3n + 1)

the logarithmic relation is:

log₂(T(n) / n) = log₂(3 + 1/n) - v₂(3n + 1)

ELA tracks the finite-block balance:

B(n₀, k) = Σ [v₂(3Tʲ(n₀)+1) - log₂(3 + 1/Tʲ(n₀))]

If:

B(n₀, k) > 0

then:

Tᵏ(n₀) < n₀

## Interpretation

ELA treats descent as an executable certificate problem.

The system records:

- the current odd integer,
- the value 3n + 1,
- the 2-adic valuation v₂,
- the next accelerated odd value,
- the local growth cost,
- the cumulative balance.

The certificate can then be replayed and verified exactly.

## Recommended Citation

Please cite the archived Zenodo record when referencing this work:

DOI: 10.5281/zenodo.20785851
