"""Reproduce Project 2 validation scenarios and write visible executed output."""

from copy import deepcopy
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


def loaded_inputs():
    """Load the committed price data and apply the documented reserve classification."""
    sleeves, correlations = estimate_from_prices(str(SOURCE_DIR / "prices.csv"))
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
    }

    output_path = PROJECT_ROOT / "output" / "validation-results.json"
    output_path.parent.mkdir(exist_ok=True)
    output_path.write_text(json.dumps(result, indent=2) + "\n", encoding="utf-8")
    print(json.dumps(result, indent=2))


if __name__ == "__main__":
    main()
