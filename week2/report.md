# Week 2 Report
Kacey Friesen
V00978721

## Steps Taken
1.  **Porting Structure:** Moved Biopython files into `code/bio_codon/motifs` and created a standalone package.
2.  **Removing C Dependencies:** Refactored `matrix.py` to remove the dependency on `_pwm` (C-module). Replaced the `calculate` method with a pure Python implementation using NumPy.
3.  **Fixing Imports:** Updated `minimal.py` and `__init__.py` to use relative imports (`from . import Motif`) instead of absolute `Bio` imports.
4.  **Testing:** Created a `test.py` compatible with both Python and Codon using the `@test` decorator pattern.

## Gotchas & Challenges
* **Zero Counts & Log-Odds:** Encountered `NaN` errors in `thresholds.py` because `log2(0)` is negative infinity. Fixed this by applying pseudocounts (`m.pseudocounts = 1.0`) in the test setup.
* **Environment:** Had to use `apt` instead of `pip` to install NumPy/Biopython on WSL due to PEP 668 managed environments.
* **Parsing:** The `minimal.py` parser had a bug reading motif names with spaces, which caused test failures.

## Time Estimate
* Approximately 5 hours
