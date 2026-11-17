# Visible Executed Output

**Run command:** `python run_validation.py`
**Run date:** 2026-11-17
**Data boundary:** Yahoo Finance monthly adjusted-close data downloaded 2026-10-22; price history through 2026-10.
**Decision:** Pilot, not adopt.

## Base case

| Allocation | Gross expected return | Annual volatility | Reserve-eligible |
|---|---:|---:|---:|
| 60% SGOV / 40% ACWI | 6.61% | 5.99% | 60% |

The base case passes the current 6.5% return objective, 3% reserve minimum, long-only rule, and 10% provisional volatility limit.

## Locked changed-input run

**Input changed:** ACWI expected annual return estimate, 10.87% to 8.00%.

| Case | Allocation | Expected return | Annual volatility | Reserve-eligible | Tested-mandate verdict |
|---|---|---:|---:|---:|---|
| Before | 60% SGOV / 40% ACWI | 6.61% | 5.99% | 60% | Pass |
| After | 35% SGOV / 65% ACWI | 6.52% | 9.65% | 35% | Pass |

The prediction that ACWI weight and volatility would increase was correct. The recommendation remains **pilot**, not adopt, because the changed mix remains below the 10% volatility limit but changes the ACWI weight by 25 percentage points.

## Additional stresses

| Stress | Result | Decision implication |
|---|---|---|
| 50 bps annual cost drag | A gross 7.00% return target produces 50% SGOV / 50% ACWI; gross return 7.32%, net return 6.82%, volatility 7.45%. | Costs make the process depend on a higher gross-return hurdle. |
| 70% reserve minimum | No feasible long-only mix reaches the 6.5% objective. | Process stop; do not recommend an allocation. |
| Last 36 months rather than full history | 85% SGOV / 15% ACWI, versus 60% / 40% in the full-history base case. | A 25-point change supports pilot rather than adoption. |

The machine-readable source of these results is [validation-results.json](validation-results.json).
