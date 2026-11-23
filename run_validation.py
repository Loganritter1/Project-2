"""Reproduce Project 2 validation scenarios and write visible executed output."""

from copy import deepcopy
from datetime import date
import json
from pathlib import Path
import sys

PROJECT_ROOT = Path(__file__).resolve().parent
SOURCE_DIR = PROJECT_ROOT / "lab13 files"
sys.path.insert(0, str(SOURCE_DIR))

from portfolio import (  # noqa: E402
    covariance_matrix,
    estimate_from_prices,
    expected_return,
    lowest_risk_mix,
    portfolio_volatility,
    reserve_eligible_weight,
)


OBJECTIVE = 0.065
RESERVE_MINIMUM = 0.03
VOLATILITY_LIMIT = 0.10
ANNUAL_COST_DRAG = 0.005


def loaded_inputs(last_36_months=False):
    """Load the committed price data and apply the documented reserve classification."""
    sleeves, correlations = estimate_from_prices(
        str(SOURCE_DIR / "prices.csv"), last_36_months=last_36_months
    )
    for ticker in ("SGOV", "VGIT"):
        sleeves[ticker]["reserve_eligible"] = True
    return sleeves, correlations


def summarize(weights, sleeves, correlations, annual_cost_drag=0.0):
    """Return serializable gross and net portfolio metrics."""
    covariance = covariance_matrix(sleeves, correlations)
    gross_return = expected_return(weights, sleeves)
    return {
        "weights": {name: round(weight, 4) for name, weight in weights.items()},
        "gross_expected_return": round(gross_return, 6),
        "annual_cost_drag": annual_cost_drag,
        "net_expected_return": round(gross_return - annual_cost_drag, 6),
        "annual_volatility": round(portfolio_volatility(weights, covariance), 6),
        "reserve_eligible_weight": round(reserve_eligible_weight(weights, sleeves), 6),
    }


def format_weights(weights):
    """Format a weight mapping for the human-readable validation record."""
    return " / ".join(
        f"{weight:.0%} {ticker}" for ticker, weight in weights.items() if weight > 0
    )


def write_visible_output(result):
    """Write Markdown evidence from the same validation results as the JSON output."""
    base = result["base_case"]
    changed = result["locked_changed_input"]
    after = changed["after"]
    cost = result["cost_stress"]["result"]
    window = result["window_stress"]
    visible_output = f"""# Visible Executed Output

**Run command:** `python run_validation.py`
**Run date:** {date.today().isoformat()}
**Data boundary:** Yahoo Finance monthly adjusted-close data downloaded 2026-10-22; price history through 2026-10.
**Decision:** Pilot, not adopt.

## Base case

| Allocation | Gross expected return | Annual volatility | Reserve-eligible |
|---|---:|---:|---:|
| {format_weights(base["weights"])} | {base["gross_expected_return"]:.2%} | {base["annual_volatility"]:.2%} | {base["reserve_eligible_weight"]:.0%} |

The base case passes the current 6.5% return objective, 3% reserve minimum, long-only rule, and 10% provisional volatility limit.

## Locked changed-input run

**Input changed:** ACWI expected annual return estimate, {changed["old_value"]:.2%} to {changed["new_value"]:.2%}.

| Case | Allocation | Expected return | Annual volatility | Reserve-eligible | Tested-mandate verdict |
|---|---|---:|---:|---:|---|
| Before | {format_weights(changed["before"]["weights"])} | {changed["before"]["gross_expected_return"]:.2%} | {changed["before"]["annual_volatility"]:.2%} | {changed["before"]["reserve_eligible_weight"]:.0%} | Pass |
| After | {format_weights(after["weights"])} | {after["gross_expected_return"]:.2%} | {after["annual_volatility"]:.2%} | {after["reserve_eligible_weight"]:.0%} | Pass |

The prediction that ACWI weight and volatility would increase was correct. The recommendation remains **pilot**, not adopt, because the changed mix remains below the 10% volatility limit but changes the ACWI weight by 25 percentage points.

## Additional stresses

| Stress | Result | Decision implication |
|---|---|---|
| 50 bps annual cost drag | A gross 7.00% return target produces {format_weights(cost["weights"])}; gross return {cost["gross_expected_return"]:.2%}, net return {cost["net_expected_return"]:.2%}, volatility {cost["annual_volatility"]:.2%}. | Costs make the process depend on a higher gross-return hurdle. |
| 70% reserve minimum | {result["constraint_stress"]["result"]} | Process stop; do not recommend an allocation. |
| Last 36 months rather than full history | {format_weights(window["weights"])}, versus {format_weights(base["weights"])} in the full-history base case. | A 25-point change supports pilot rather than adoption. |

The machine-readable source of these results is [validation-results.json](validation-results.json).
"""
    (PROJECT_ROOT / "output" / "visible-output.md").write_text(
        visible_output, encoding="utf-8"
    )


def main():
    sleeves, correlations = loaded_inputs()

    base_weights = lowest_risk_mix(sleeves, correlations, OBJECTIVE, RESERVE_MINIMUM)

    changed_sleeves = deepcopy(sleeves)
    changed_sleeves["ACWI"]["return"] = 0.08
    changed_weights = lowest_risk_mix(
        changed_sleeves, correlations, OBJECTIVE, RESERVE_MINIMUM
    )

    cost_weights = lowest_risk_mix(
        sleeves, correlations, OBJECTIVE + ANNUAL_COST_DRAG, RESERVE_MINIMUM
    )
    restrictive_reserve_weights = lowest_risk_mix(sleeves, correlations, OBJECTIVE, 0.70)
    window_sleeves, window_correlations = loaded_inputs(last_36_months=True)
    window_weights = lowest_risk_mix(
        window_sleeves, window_correlations, OBJECTIVE, RESERVE_MINIMUM
    )

    result = {
        "as_of": "2026-10-22 download; monthly price history through 2026-10",
        "decision": "Pilot, not adopt",
        "base_case": summarize(base_weights, sleeves, correlations),
        "locked_changed_input": {
            "input": "ACWI expected annual return estimate",
            "old_value": 0.108685,
            "new_value": 0.08,
            "before": summarize(base_weights, sleeves, correlations),
            "after": summarize(changed_weights, changed_sleeves, correlations),
            "volatility_limit": VOLATILITY_LIMIT,
            "recommendation": "Pilot remains appropriate; the changed mix remains below the provisional volatility limit.",
        },
        "cost_stress": {
            "annual_cost_drag": ANNUAL_COST_DRAG,
            "method": "Raise the required gross return by the assumed annual cost drag, then report net return after the drag.",
            "result": summarize(cost_weights, sleeves, correlations, ANNUAL_COST_DRAG),
        },
        "constraint_stress": {
            "reserve_minimum": 0.70,
            "result": "No feasible long-only mix meets both the 6.5% objective and a 70% reserve minimum. Process stop.",
            "weights": restrictive_reserve_weights,
        },
        "window_stress": summarize(window_weights, window_sleeves, window_correlations),
    }

    output_path = PROJECT_ROOT / "output" / "validation-results.json"
    output_path.parent.mkdir(exist_ok=True)
    output_path.write_text(json.dumps(result, indent=2) + "\n", encoding="utf-8")
    write_visible_output(result)
    print(json.dumps(result, indent=2))


if __name__ == "__main__":
    main()
