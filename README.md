# xfoil-init: Learned Initializer for XFoil

A neural network that predicts a starting boundary-layer state for XFoil-class viscous-inviscid airfoil solvers, so the solver converges more reliably and with less total work.

## Why

XFoil solves for the boundary-layer state (θ, δ*, Ue, Ctau/n at every station) with a Newton iteration, and that iteration needs a starting guess.

- A cold start converged for 84% of low-Reynolds test points in our probe. Continuation (warm start from a neighbouring α) reached 91%.
- Continuation needs an extra solve for the neighbouring point, and it fails on unordered or jumping queries.
- A model that predicts a good starting state directly from (shape, α, Re) could avoid both problems.

## Research question

Can a learned generator of starting states reduce solver failures and end-to-end cost, at unchanged acceptance standards, on airfoil families the model has not seen?

Important factors:

- acceptance rate
- Newton iterations
- time per accepted solve: preprocessing + inference + state mapping + solver + fallback
- agreement with the reference solution

## Architecture Proposal

## Existing scripts

## Setup notes

## Status

Early stage. More to come...

