# Learned XFoil Starting-State Optimizer

A neural network that predicts a starting boundary-layer state for XFoil-class viscous-inviscid airfoil solvers, so the solver converges more reliably and with less total work.

Why

XFoil solves for the boundary-layer state (θ, δ*, Ue, Ctau/n at every station) with a Newton iteration, and that iteration needs a starting guess.

A cold start converged for 84% of low-Reynolds test points in our probe. Continuation (warm start from a neighbouring α) reached 91%.
Continuation needs an extra solve for the neighbouring point, and it fails on unordered or jumping queries.
A model that predicts a good starting state directly from (shape, α, Re) could avoid both problems.
Research question

Can a learned generator of starting states reduce solver failures and end-to-end cost, at unchanged acceptance standards, on airfoil families the model has not seen?

Success is measured by solver behaviour, not by prediction error:

acceptance rate
Newton iterations
time per accepted solve: preprocessing + inference + state mapping + solver + fallback
agreement with the reference solution
Plan
Stage	What	Gate
0	State adapter: read XFoil's state, resample to a fixed grid, inject it back	G1: round trip converges to the same solution
1	Dataset: UIUC airfoils + CST augmentation, split by airfoil family	
2	Baselines: cold, continuation, nearest stored state, interpolation, NeuralFoil adapter	
3	K=1 PyTorch model, solver-in-the-loop evaluation	G2: beats the baselines on held-out airfoils
4	Native C++ runtime, latency and precision study	
5	Optional: K>1 multi-solution extension	G3: enough robust branches

Full plan: see the project plan doc.

Layout (proposed)
xfoil-init/
  data/        generated runs, splits (by airfoil family)
  adapter/     XFoil state read/inject, grid resampling, round-trip test
  baselines/   cold, continuation, nearest, interpolation, NeuralFoil
  models/      PyTorch model, losses, training loop
  eval/        end-to-end solver benchmark
  cpp/         native inference runtime
  scripts/     probes and tests (see below)
Existing scripts
File	Purpose
xfoil_init_probe.py	Cold start vs α-sweep convergence
xfoil_warmstart_tests.py	Basin-of-attraction test, NeuralFoil boundary-layer distance, up/down sweep
xfoil_branch_census.py	Counts distinct solver-accepted solutions per condition
xfoil_pert.patch	Adds a PERT command to XFoil to perturb the starting state
Setup notes
Ubuntu's xfoil package is built with floating-point traps and crashes with SIGFPE in batch use. The scripts compile a small LD_PRELOAD shim that disables the traps (Linux, needs gcc).
XFoil can hang after divergence, so every run needs a timeout.
"MRCHDU: Convergence failed" is not a failure. Only "VISCAL: Convergence failed" means the Newton solve failed.
Results depend on the panel count. Use the same paneling throughout.
Status

Early stage. Probe results exist; the adapter and trained model do not. Resume and report numbers stay as placeholders until measured.

Caveats
Branch census numbers were computed at a single paneling (N=160) and are an upper bound until checked at other panel counts.
Simple baselines (nearest stored state, a NeuralFoil adapter) may capture most of the benefit. That outcome is reportable, not a failure.
Use "solver-accepted solutions", not "real stall hysteresis".
