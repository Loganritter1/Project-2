# Validation and AI Use

## AI use, authorship, and boundary

I used OpenAI Codex (GPT-5) from 2026-11-17 through 2026-11-23 to explain course requirements, plan the application structure, improve Streamlit code, improve the app's visual presentation, and prepare submission documentation. I reviewed the resulting code and calculations, selected the inputs and process, and remain responsible for the analysis and decision.

This analysis is for education only and is not investment advice.

## Decision scope and data boundary

This application compares equal-weight, inverse-volatility, and 60/40 benchmark portfolios with a constrained lowest-risk portfolio for the Meridian Foundation Reserve. The constrained portfolio is long-only and is tested against a 6.5% expected-return objective, a 3% reserve-eligible minimum, and a provisional 10% annual-volatility limit.

The point-in-time input is a trailing historical-return signal, not a forward-looking forecast. `lab13 files/prices.csv` contains monthly adjusted-close prices for SGOV, VGIT, VCIT, and ACWI from October 2021 through October 2026, downloaded from Yahoo Finance on 2026-10-22. The app calculates simple monthly returns, annualizes their mean by multiplying by 12, and annualizes sample volatility by multiplying by the square root of 12. The full-history and trailing-36-month windows are both shown because the result is sensitive to the estimation window.

## Completed checks and results

| Check | Result | Interpretation |
|---|---|---|
| App startup | Streamlit 1.66.0 is installed and the app compiles. | The README command can start the web app locally. |
| Full-history result from committed price data | 60% SGOV / 40% ACWI; 6.61% estimated return; 5.99% annual volatility; 60% reserve-eligible. | The constrained portfolio meets the currently tested return, reserve, volatility, and long-only rules. |
| Transparent baselines | Equal-weight and inverse-volatility portfolios are displayed beside the constrained portfolio, each with a rule-by-rule pass/fail verdict. | The proposed process can be compared to two reproducible alternatives. |
| Input validation | `portfolio.py` rejects correlation values outside -1 to 1 and non-symmetric correlation tables; it also checks price-file completeness and positive prices. | Invalid inputs should stop calculation rather than silently produce a result. |
| Known-answer reconciliation | The course training covariance for Treasury 10-year notes and investment-grade bonds is `0.80 x 0.07 x 0.06 = 0.00336`. | The automated known-answer test reproduces 0.00336 from the displayed correlation and volatility inputs. |
| Estimate stress | With the training assumption for global equity return reduced from 8.0% to 7.0%, the lowest-risk mix changed from 0/20/25/55 to 0/10/10/80, and volatility rose from 9.44% to 12.94%. | Small return-estimate changes can materially change the selected mix and can breach the provisional risk limit. |
| Window stress | The committed five-year result is 60% SGOV / 40% ACWI; the last-36-month result is 85% SGOV / 15% ACWI. | The 25-percentage-point allocation change supports a pilot rather than immediate adoption. |
| Cost stress | A 50-basis-point annual cost drag raises the gross return hurdle to 7.0%. The lowest-risk mix becomes 50% SGOV / 50% ACWI, with 7.32% gross return, 6.82% net return, and 7.45% volatility. | A live allocation requires costs to be modelled and approved rather than assumed away. |
| Constraint stress | Raising the reserve minimum from 3% to 70% produces no feasible long-only mix that reaches the 6.5% objective. | The process stops rather than presenting an ineligible allocation. |
| Fresh-clone check | A fresh GitHub clone at commit `20e82e0` passed dependency verification, all seven tests, and the validation runner. | A clean user can reproduce the visible result without manual repair. |

## AI-output check

| AI-assisted claim considered | Independent check | Disposition | Effect on decision |
|---|---|---|---|
| An invalid correlation table should stop the portfolio calculation rather than create a covariance matrix silently. | `tests/test_portfolio.py` changes one correlation-table cell so the table is asymmetric and confirms `ValueError`; the known-answer covariance-cell test separately confirms the valid calculation. | Accepted only after the tests passed. | Supports the reliability of the calculation gate, but does not validate the return forecasts or justify adoption. |

## Limitations, stress boundary, and process stop

The current app does not model transaction costs, taxes, bid-ask spreads, capacity, or turnover from prior holdings. The 50-basis-point cost stress is an analytical hurdle test, not an estimate of Meridian's actual costs. Therefore the app must not be treated as an adoption-ready live allocation engine.

The app's displayed mandate verdict covers only long-only status, expected return, reserve eligibility, and the provisional volatility limit. Lab 13 liquidity, issuer-concentration, and turnover rules require either additional portfolio-security/trading data or an explicit final-policy treatment before adoption.

Stop the process and do not recommend an allocation if no long-only portfolio can meet the return and reserve requirements, if the proposed portfolio fails a tested mandate rule, or if cost/constraint evidence materially changes the recommendation. Review the data, assumptions, implementation costs, and mandate before rerunning the process.

## Locked Changed-Input Record

- **Input:** ACWI expected annual return estimate.
- **Old value:** 10.87% per year.
- **New value:** 8.0% per year.
- **Prediction:** Lowering ACWI's expected return from 10.87% to 8.0% will require more ACWI in the constrained mix to reach the 6.5% return objective. I expect annual portfolio volatility to increase. The recommendation may change from pilot to stop/reject if the increased volatility exceeds the 10.0% provisional limit.
- **Prediction written on:** 11/17/2026, 1:45 PM.
- **Pre-run commit and GitHub link:** `386943d90e312b8c32f4dca6f53724f18b03b873` — <https://github.com/Loganritter1/Project-2/blob/386943d90e312b8c32f4dca6f53724f18b03b873/docs/validation-and-ai-use.md>

### Post-run result — complete only after the pre-run commit

- **Run date and time:** 11/17/2026, after pre-run snapshot `386943d`.
- **Before allocation / return / volatility:** 60% SGOV / 40% ACWI; 6.61%; 5.99%.
- **After allocation / return / volatility:** 35% SGOV / 65% ACWI; 6.52%; 9.65%.
- **Mandate verdict before and after:** Pass before and after: the return objective, reserve minimum, long-only rule, and 10% provisional volatility limit all pass.
- **Did the recommendation change?** No. The process remains a pilot, not an adoption-ready allocation process.
- **Why the result matched or differed from the prediction:** The ACWI weight increased from 40% to 65% and volatility increased from 5.99% to 9.65%, matching the predicted direction. The volatility limit was not breached, so the expected stop/reject condition did not occur. The 25-point allocation shift still demonstrates material estimation sensitivity.
