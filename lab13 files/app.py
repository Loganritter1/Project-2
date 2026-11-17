"""Lab 15: Streamlit interface for the portfolio stability decision."""

from copy import deepcopy
import csv

import altair as alt
import pandas as pd
import streamlit as st

from portfolio import (
    CORRELATIONS,
    OBJECTIVE_RETURN,
    SLEEVES,
    estimate_from_prices,
    expected_return,
    lowest_risk_mix,
    portfolio_volatility,
    covariance_matrix,
    equal_weight_portfolio,
    reserve_eligible_weight,
    inverse_volatility_portfolio,
)


def metrics(weights, sleeves, correlations):
    """Return the displayed portfolio metrics using portfolio.py calculations."""
    covariance = covariance_matrix(sleeves, correlations)
    return {
        "return": expected_return(weights, sleeves),
        "volatility": portfolio_volatility(weights, covariance),
        "reserve": reserve_eligible_weight(weights, sleeves),
    }


def show_answer(title, weights, sleeves, correlations):
    """Show an allocation and its calculated metrics, or the infeasible message."""
    st.subheader(title)
    if weights is None:
        st.warning("No mix meets the objective.")
        return

    result = metrics(weights, sleeves, correlations)
    st.dataframe(
        {
            "Asset": list(weights),
            "Weight": [f"{weight:.0%}" for weight in weights.values()],
        },
        hide_index=True,
        width="stretch",
    )
    first, second, third = st.columns(3)
    first.metric("Expected return", f"{result['return']:.2%}")
    second.metric("Volatility", f"{result['volatility']:.2%}")
    third.metric("Reserve-eligible", f"{result['reserve']:.0%}")


def mandate_failures(weights, sleeves, correlations, objective, reserve_minimum, volatility_limit):
    """Return the app-level mandate failures for a fully specified portfolio."""
    result = metrics(weights, sleeves, correlations)
    failures = []
    if abs(sum(weights.values()) - 1) > 1e-9:
        failures.append("weights do not total 100%")
    if any(weight < 0 for weight in weights.values()):
        failures.append("not long-only")
    if result["return"] < objective:
        failures.append("below return objective")
    if result["reserve"] < reserve_minimum:
        failures.append("below reserve minimum")
    if result["volatility"] > volatility_limit:
        failures.append("above volatility limit")
    return failures


def allocation_bar(weights):
    """Render a compact, labeled allocation bar for a portfolio."""
    palette = {
        "Treasury bills": "#f7bd35",
        "Treasury 10-year note": "#6ba8ff",
        "Investment-grade bond fund": "#a78bfa",
        "Global equity index fund": "#31d49a",
    }
    segments = []
    labels = []
    for asset, weight in weights.items():
        if weight <= 0:
            continue
        color = palette.get(asset, "#92a4b7")
        segments.append(f'<span style="width:{weight * 100:.1f}%;background:{color}" title="{asset}: {weight:.0%}"></span>')
        labels.append(f'<span><i style="background:{color}"></i>{asset} {weight:.0%}</span>')
    st.markdown(
        '<div class="allocation-bar" aria-label="Portfolio allocation">' + "".join(segments) + "</div>"
        + '<div class="allocation-legend">' + "".join(labels) + "</div>",
        unsafe_allow_html=True,
    )


def mandate_scorecard(weights, sleeves, correlations, objective, reserve_minimum, volatility_limit):
    """Render the four tested mandate rules as a compact decision scorecard."""
    result = metrics(weights, sleeves, correlations)
    checks = [
        ("Return", result["return"] >= objective, f"{result['return']:.2%} / {objective:.2%}"),
        ("Reserve", result["reserve"] >= reserve_minimum, f"{result['reserve']:.0%} / {reserve_minimum:.0%}"),
        ("Risk", result["volatility"] <= volatility_limit, f"{result['volatility']:.2%} / {volatility_limit:.2%}"),
        ("Long-only", all(weight >= 0 for weight in weights.values()), "No short positions"),
    ]
    tiles = []
    for label, passed, detail in checks:
        state = "pass" if passed else "fail"
        status = "PASS" if passed else "FAIL"
        tiles.append(f'<div class="rule-tile {state}"><b>{label}</b><strong>{status}</strong><small>{detail}</small></div>')
    st.markdown('<div class="rule-grid">' + "".join(tiles) + "</div>", unsafe_allow_html=True)


def benchmark_portfolio(sleeves):
    """Build the stated 60/40 global-equity / investment-grade-bond benchmark."""
    equity = next((name for name in sleeves if name in {"Global equity index fund", "ACWI"}), None)
    bonds = next((name for name in sleeves if name in {"Investment-grade bond fund", "VCIT"}), None)
    if equity is None or bonds is None:
        return None
    return {name: 0.60 if name == equity else 0.40 if name == bonds else 0.0 for name in sleeves}


def uploaded_data_card(uploaded_bytes):
    """Return source fields for the uploaded CSV without changing its calculations."""
    rows = list(csv.DictReader(uploaded_bytes.decode("utf-8-sig").splitlines()))
    if not rows:
        return "—", "—", "0 monthly prices"
    dates = list(rows[0])
    date_column = dates[0]
    return rows[0][date_column], rows[-1][date_column], f"{max(len(rows) - 1, 0)} monthly returns"


def reset_input_controls():
    """Clear editable assumptions so Streamlit restores their displayed defaults."""
    exact_keys = {"objective_input", "reserve_minimum_input", "volatility_limit_input"}
    for key in list(st.session_state):
        if key in exact_keys or key.startswith("return_") or key.startswith("reserve_"):
            del st.session_state[key]
    st.session_state["input_version"] = st.session_state.get("input_version", 0) + 1
    st.session_state["reset_notice"] = True


def show_portfolio(title, weights, sleeves, correlations, objective, reserve_minimum, volatility_limit):
    """Show a portfolio and its explicit pass/fail mandate verdict."""
    with st.container(border=True):
        show_answer(title, weights, sleeves, correlations)
        if weights is None:
            return
        allocation_bar(weights)
        failures = mandate_failures(
            weights, sleeves, correlations, objective, reserve_minimum, volatility_limit
        )
        mandate_scorecard(weights, sleeves, correlations, objective, reserve_minimum, volatility_limit)
        if failures:
            st.error("Mandate: FAIL — " + "; ".join(failures) + ".")
        else:
            st.success("Mandate: PASS — all tested rules pass.")


st.set_page_config(page_title="Portfolio Stability Decision", layout="wide")
st.markdown(
    """
    <style>
        :root {
            --terminal-bg: #080d14;
            --panel: #111b27;
            --panel-border: #27384b;
            --ink: #e8eff7;
            --muted: #92a4b7;
            --market-yellow: #f7bd35;
            --market-green: #31d49a;
            --market-red: #ff6b6b;
        }
        .stApp { background: var(--terminal-bg); color: var(--ink); }
        [data-testid="stHeader"] { background: rgba(8, 13, 20, 0.92); }
        [data-testid="stSidebar"] { background: #0c131d; border-right: 1px solid var(--panel-border); }
        [data-testid="stSidebar"] * { color: var(--ink); }
        [data-testid="stSidebar"] .stNumberInput label { color: var(--muted); font-size: 0.83rem; }
        .dashboard-hero {
            background: linear-gradient(115deg, #121e2c 0%, #0d1722 52%, #18283a 100%);
            border: 1px solid #31465e;
            border-left: 5px solid var(--market-yellow);
            border-radius: 12px;
            padding: 1.5rem 1.65rem 1.25rem;
            margin: 0.4rem 0 1.15rem;
        }
        .eyebrow { color: var(--market-yellow); font-family: monospace; font-size: 0.78rem; font-weight: 700; letter-spacing: 0.13em; }
        .dashboard-hero h1 { color: #ffffff; font-size: 2.1rem; line-height: 1.1; margin: 0.35rem 0 0.45rem; }
        .dashboard-hero p { color: var(--muted); font-size: 0.95rem; margin: 0; }
        h1, h2, h3 { color: var(--ink) !important; }
        h2 { border-bottom: 1px solid var(--panel-border); padding-bottom: 0.4rem; }
        [data-testid="stMetric"] {
            background: #0b1520;
            border: 1px solid #263b50;
            border-radius: 8px;
            padding: 0.65rem 0.7rem;
        }
        [data-testid="stMetricLabel"] { color: var(--muted); }
        [data-testid="stMetricValue"] { color: #f4f8fc; font-family: monospace; }
        [data-testid="stVerticalBlockBorderWrapper"] {
            background: var(--panel);
            border-color: var(--panel-border) !important;
            box-shadow: 0 10px 20px rgba(0,0,0,.18);
        }
        [data-testid="stDataFrame"] { border: 1px solid #263b50; border-radius: 7px; overflow: hidden; }
        .stAlert { border-radius: 7px; }
        [data-testid="stCaptionContainer"] { color: var(--muted); }
        .stButton button, [data-testid="stFileUploader"] button {
            background: #1b3045; border: 1px solid #3a5875; color: #eef6ff;
        }
        .allocation-bar { display: flex; height: 12px; overflow: hidden; border-radius: 6px; background: #243544; margin: 0.65rem 0 0.4rem; }
        .allocation-bar span { display: block; min-width: 0; }
        .allocation-legend { display: flex; flex-wrap: wrap; gap: 0.35rem 0.7rem; margin-bottom: 0.7rem; color: var(--muted); font-size: 0.76rem; }
        .allocation-legend span { white-space: nowrap; }
        .allocation-legend i { display: inline-block; width: 0.55rem; height: 0.55rem; border-radius: 50%; margin-right: 0.25rem; }
        .rule-grid { display: grid; grid-template-columns: repeat(2, minmax(0, 1fr)); gap: 0.35rem; margin: 0.65rem 0 0.15rem; }
        .rule-tile { padding: 0.42rem 0.5rem; background: #0b1520; border-left: 3px solid #506477; }
        .rule-tile.pass { border-left-color: var(--market-green); }
        .rule-tile.fail { border-left-color: var(--market-red); }
        .rule-tile b, .rule-tile strong, .rule-tile small { display: block; }
        .rule-tile b { color: var(--muted); font-size: 0.7rem; font-weight: 500; text-transform: uppercase; letter-spacing: 0.05em; }
        .rule-tile strong { color: var(--ink); font-family: monospace; font-size: 0.8rem; }
        .rule-tile small { color: var(--muted); font-size: 0.7rem; }
    </style>
    <div class="dashboard-hero">
        <div class="eyebrow">MERIDIAN FOUNDATION // DECISION DESK</div>
        <h1>Portfolio Stability Decision</h1>
        <p>Compare transparent baselines with a constrained portfolio under the current mandate assumptions.</p>
    </div>
    """,
    unsafe_allow_html=True,
)
st.caption("Educational demonstration, not investment advice. AI assisted the code build; the analysis and decision are the student's work.")

with st.sidebar:
    st.header("Mandate controls")
    objective = st.number_input(
        "Objective return estimate (%)", value=OBJECTIVE_RETURN * 100, step=0.1, key="objective_input"
    ) / 100
    reserve_minimum = st.number_input(
        "Minimum reserve-eligible weight (%)", value=3.0, min_value=0.0, max_value=100.0, step=1.0, key="reserve_minimum_input"
    ) / 100
    volatility_limit = st.number_input(
        "Provisional annual-volatility limit (%)", value=10.0, min_value=0.1, max_value=100.0, step=0.5, key="volatility_limit_input"
    ) / 100
    uploaded_file = st.file_uploader("Upload monthly prices.csv", type="csv")
    last_36_months = st.toggle("Use last 36 monthly returns", value=False)

if uploaded_file is None:
    source_name = "Meridian training inputs"
    first_observation, last_observation, observation_count = "Training assumption set", "Not applicable", "Not applicable"
    loaded_sleeves = deepcopy(SLEEVES)
    loaded_correlations = deepcopy(CORRELATIONS)
    active_sleeves = deepcopy(loaded_sleeves)
    active_correlations = loaded_correlations
else:
    try:
        source_name = "Uploaded prices.csv"
        uploaded_bytes = uploaded_file.getvalue()
        first_observation, last_observation, observation_count = uploaded_data_card(uploaded_bytes)
        loaded_sleeves, loaded_correlations = estimate_from_prices(uploaded_bytes)
        if last_36_months:
            active_sleeves, active_correlations = estimate_from_prices(
                uploaded_bytes, last_36_months=True
            )
        else:
            active_sleeves = deepcopy(loaded_sleeves)
            active_correlations = loaded_correlations
    except ValueError as error:
        st.error(f"Could not estimate from this CSV: {error}")
        st.stop()

# Preserve the known reserve classification when this project's ETF tickers are uploaded.
for sleeve_set in (loaded_sleeves, active_sleeves):
    for ticker in ("SGOV", "VGIT"):
        if ticker in sleeve_set:
            sleeve_set[ticker]["reserve_eligible"] = True

st.write(f"**Data source:** {source_name}. Returns shown are historical estimates, not forecasts.")
st.info("Current scope: the benchmark is 60% global equities / 40% investment-grade bonds. The app tests long-only, return, reserve, and provisional volatility rules. Confirm or replace provisional terms before the final project.")
data_left, data_middle, data_right = st.columns(3)
data_left.metric("Input mode", "Uploaded CSV" if uploaded_file else "Training inputs")
data_middle.metric("Asset sleeves", len(active_sleeves))
data_right.metric("Estimation window", "Last 36 months" if last_36_months and uploaded_file else "Full available history")
with st.expander("Data card"):
    st.write(f"**Source:** {source_name}")
    st.write(f"**First observation:** {first_observation}")
    st.write(f"**Last observation:** {last_observation}")
    st.write(f"**Coverage:** {observation_count}")
    st.write("**Method:** simple monthly returns, annualized as monthly mean × 12; annual volatility uses monthly sample standard deviation × √12.")
st.subheader("Editable inputs")
st.caption("Edit an expected return estimate or reserve eligibility to test stability.")

st.button("Reset editable assumptions", on_click=reset_input_controls)
if st.session_state.pop("reset_notice", False):
    st.success("Editable return, reserve, objective, and volatility inputs were reset to their defaults.")

input_columns = st.columns(2)
input_version = st.session_state.get("input_version", 0)
for index, asset in enumerate(active_sleeves):
    with input_columns[index % 2]:
        active_sleeves[asset]["return"] = st.number_input(
            f"{asset} expected return estimate (%)",
            value=active_sleeves[asset]["return"] * 100,
            step=0.1,
            key=f"return_{source_name}_{last_36_months}_{asset}_{input_version}",
        ) / 100
        active_sleeves[asset]["reserve_eligible"] = st.checkbox(
            f"{asset} is reserve-eligible",
            value=active_sleeves[asset]["reserve_eligible"],
            key=f"reserve_{source_name}_{last_36_months}_{asset}_{input_version}",
        )

baseline_sleeves = deepcopy(loaded_sleeves)
for asset in baseline_sleeves:
    baseline_sleeves[asset]["reserve_eligible"] = active_sleeves[asset]["reserve_eligible"]

loaded_answer = lowest_risk_mix(
    baseline_sleeves, loaded_correlations, objective, reserve_minimum
)
active_answer = lowest_risk_mix(
    active_sleeves, active_correlations, objective, reserve_minimum
)

equal_weight = equal_weight_portfolio(active_sleeves)
inverse_volatility = inverse_volatility_portfolio(active_sleeves)
benchmark = benchmark_portfolio(active_sleeves)

st.header("Portfolio comparison")
first, second = st.columns(2)
with first:
    show_portfolio("Baseline 1: equal weight", equal_weight, active_sleeves, active_correlations, objective, reserve_minimum, volatility_limit)
with second:
    show_portfolio("Baseline 2: inverse volatility", inverse_volatility, active_sleeves, active_correlations, objective, reserve_minimum, volatility_limit)
third, fourth = st.columns(2)
with third:
    show_portfolio("Benchmark: 60% equity / 40% IG bonds", benchmark, active_sleeves, active_correlations, objective, reserve_minimum, volatility_limit)
with fourth:
    show_portfolio("Proposed: constrained lowest-risk mix", active_answer, active_sleeves, active_correlations, objective, reserve_minimum, volatility_limit)

if active_answer is None:
    st.error("PROCESS STOPPED: no long-only mix meets both the return objective and reserve minimum. Do not recommend an allocation until the inputs or mandate are reviewed.")
else:
    failures = mandate_failures(active_answer, active_sleeves, active_correlations, objective, reserve_minimum, volatility_limit)
    if failures:
        st.error("PROCESS STOPPED: the proposed mix fails a tested mandate rule. Do not recommend an allocation until the failed rule(s) are resolved.")
    else:
        st.info("Provisional decision: pilot the constrained process; do not adopt until the point-in-time signal, data card, and stress evidence are complete.")

    top_assets = sorted(active_answer.items(), key=lambda item: item[1], reverse=True)
    primary_asset, primary_weight = top_assets[0]
    reserve_weight = reserve_eligible_weight(active_answer, active_sleeves)
    st.markdown(
        f"### Why this mix?\n"
        f"The engine selects the lowest-volatility eligible mix that clears the return objective. "
        f"Its largest allocation is **{primary_asset} ({primary_weight:.0%})**; the mix keeps "
        f"**{reserve_weight:.0%}** in reserve-eligible assets while targeting **{objective:.2%}** expected return."
    )

chart_rows = []
for name, weights in {
    "Equal weight": equal_weight,
    "Inverse volatility": inverse_volatility,
    "60/40 benchmark": benchmark,
    "Constrained mix": active_answer,
}.items():
    if weights is None:
        continue
    result = metrics(weights, active_sleeves, active_correlations)
    status = "Pass" if not mandate_failures(
        weights, active_sleeves, active_correlations, objective, reserve_minimum, volatility_limit
    ) else "Fail"
    chart_rows.append({"Portfolio": name, "Volatility": result["volatility"], "Expected return": result["return"], "Mandate": status})

if chart_rows:
    st.header("Risk / return map")
    chart_data = pd.DataFrame(chart_rows)
    points = alt.Chart(chart_data).mark_circle(size=190).encode(
        x=alt.X("Volatility:Q", axis=alt.Axis(format="%", title="Annual volatility")),
        y=alt.Y("Expected return:Q", axis=alt.Axis(format="%", title="Expected annual return")),
        color=alt.Color("Mandate:N", scale=alt.Scale(domain=["Pass", "Fail"], range=["#31d49a", "#ff6b6b"])),
        tooltip=["Portfolio:N", alt.Tooltip("Expected return:Q", format=".2%"), alt.Tooltip("Volatility:Q", format=".2%"), "Mandate:N"],
    )
    labels = alt.Chart(chart_data).mark_text(align="left", dx=9, dy=-8, color="#e8eff7").encode(
        x="Volatility:Q", y="Expected return:Q", text="Portfolio:N"
    )
    return_rule = alt.Chart(pd.DataFrame({"target": [objective]})).mark_rule(color="#f7bd35", strokeDash=[5, 5]).encode(y="target:Q")
    risk_rule = alt.Chart(pd.DataFrame({"limit": [volatility_limit]})).mark_rule(color="#6ba8ff", strokeDash=[5, 5]).encode(x="limit:Q")
    st.altair_chart((return_rule + risk_rule + points + labels).properties(height=310), width="stretch")
    st.caption("Gold dashed line: return objective. Blue dashed line: provisional volatility limit. Hover over a point for exact values.")

if active_answer is not None and loaded_answer is not None:
    largest_change = max(
        abs(active_answer[asset] - loaded_answer[asset]) for asset in active_answer
    )
    before = metrics(loaded_answer, baseline_sleeves, loaded_correlations)
    after = metrics(active_answer, active_sleeves, active_correlations)
    st.header("Scenario comparison")
    scenario = pd.DataFrame(
        [
            {"Measure": "Expected return", "Inputs as loaded": f"{before['return']:.2%}", "Current edits": f"{after['return']:.2%}"},
            {"Measure": "Annual volatility", "Inputs as loaded": f"{before['volatility']:.2%}", "Current edits": f"{after['volatility']:.2%}"},
            {"Measure": "Reserve-eligible", "Inputs as loaded": f"{before['reserve']:.0%}", "Current edits": f"{after['reserve']:.0%}"},
        ]
    )
    st.dataframe(scenario, hide_index=True, width="stretch")
    st.info(f"Largest allocation change from the loaded answer: {largest_change:.0%} points. Use this panel to document the Locked Changed-Input Record.")
