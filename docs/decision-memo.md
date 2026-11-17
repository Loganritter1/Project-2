# Meridian Foundation Reserve: Decision Memo

**AI use:** OpenAI Codex (GPT-5) assisted with explaining requirements, planning the app, improving the Streamlit code, and improving presentation. **Authorship and boundary:** I reviewed the code and calculations, selected the inputs and process, and remain responsible for the analysis and decision. This analysis is for education only and is not investment advice.

## Decision and committee ask

**Recommendation: approve a non-funded pilot; do not adopt the allocation process for live capital yet.** The committee should authorize validation of the constrained lowest-volatility method, not a permanent allocation. For the analytical pilot, examine the 35% to 65% ACWI range paired with the remaining balance in SGOV; this is a sensitivity range, not a funded mandate.

## Evidence and current result

Using Yahoo Finance monthly adjusted-close data downloaded 2026-10-22, the five-year historical estimate produces a 60% SGOV / 40% ACWI constrained mix. It has a 6.61% gross expected return, 5.99% annual volatility, and 60% reserve-eligible weight. It passes the current 6.5% return objective, 3% reserve minimum, long-only rule, and 10% provisional volatility limit.

The app compares that mix against equal-weight and inverse-volatility baselines, each with an explicit mandate verdict. The app uses 5-percentage-point allocation increments, so the result is a transparent grid-search solution rather than false continuous-optimization precision.

## Material sensitivities and risks

- Lowering ACWI's expected annual return from 10.87% to 8.00% changes the proposed mix to 35% SGOV / 65% ACWI. Expected return is 6.52% and volatility is 9.65%. The mix still passes, but the 25-point weight change demonstrates estimation sensitivity.
- Restricting the sample to the latest 36 monthly returns changes the mix to 85% SGOV / 15% ACWI. That is another 25-point allocation shift.
- Applying a 50-basis-point annual cost drag requires a 7.0% gross hurdle. The selected mix becomes 50% SGOV / 50% ACWI with a 6.82% net expected return. This is a stress test, not an estimate of live costs.
- A 70% reserve minimum makes the process infeasible at the 6.5% return objective. The correct response is a process stop, not an ineligible allocation.

The model's historical returns, volatilities, and correlations are estimates rather than forecasts. It does not yet model actual transaction costs, taxes, bid-ask spreads, capacity, turnover from prior holdings, or all Lab 13 liquidity and issuer constraints.

## Conditions, monitoring, and reversal trigger

The pilot owner should rerun the evidence when the price window changes, the return estimate changes by one percentage point, the reserve requirement changes, or implementation costs can be estimated from an actual trading plan. Monitor allocation change, expected return, annual volatility, reserve-eligible weight, and each mandate verdict.

Reverse the pilot recommendation and stop the process if no long-only mix satisfies the return and reserve requirements, if the proposed mix breaches a tested rule, or if actual costs/constraints make the process infeasible. Adoption requires a documented point-in-time signal policy, approved cost assumptions, and a complete treatment of the remaining mandate rules.
