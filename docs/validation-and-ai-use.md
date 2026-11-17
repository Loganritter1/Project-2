# Validation and AI Use

## AI use, authorship, and boundary

I used OpenAI Codex (GPT-5) on 2026-11-17 to explain course requirements, plan the application structure, improve Streamlit code, and improve the app's visual presentation. I reviewed the resulting code and calculations, selected the inputs and process, and remain responsible for the analysis and decision.

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
| Estimate stress | With the training assumption for global equity return reduced from 8.0% to 7.0%, the lowest-risk mix changed from 0/20/25/55 to 0/10/10/80, and volatility rose from 9.44% to 12.94%. | Small return-estimate changes can materially change the selected mix and can breach the provisional risk limit. |
| Window stress | The committed five-year result is 60% SGOV / 40% ACWI; the last-36-month result is 85% SGOV / 15% ACWI. | The 25-percentage-point allocation change supports a pilot rather than immediate adoption. |

## Limitations, stress boundary, and process stop

The current app does not model transaction costs, taxes, bid-ask spreads, capacity, or turnover from prior holdings. Therefore the return objective is gross of those implementation costs, and the app must not be treated as an adoption-ready live allocation engine. A separate cost and constraint stress is still required before any adoption recommendation.

The app's displayed mandate verdict covers only long-only status, expected return, reserve eligibility, and the provisional volatility limit. Lab 13 liquidity, issuer-concentration, and turnover rules require either additional portfolio-security/trading data or an explicit final-policy treatment before adoption.

Stop the process and do not recommend an allocation if no long-only portfolio can meet the return and reserve requirements, if the proposed portfolio fails a tested mandate rule, or if cost/constraint evidence materially changes the recommendation. Review the data, assumptions, implementation costs, and mandate before rerunning the process.

## Locked Changed-Input Record

- **Input:** ACWI expected annual return estimate.
- **Old value:** 10.87% per year.
- **New value:** 8.0% per year.
- **Prediction:** Lowering ACWI's expected return from 10.87% to 8.0% will require more ACWI in the constrained mix to reach the 6.5% return objective. I expect annual portfolio volatility to increase. The recommendation may change from pilot to stop/reject if the increased volatility exceeds the 10.0% provisional limit.
- **Prediction written on:** 11/17/2026, 1:45 PM.
- **Pre-run commit and GitHub link:** `386943d90e312b8c32f4dca6f53724f18b03b873` — <https://github.com/Loganritter1/Project-2/blob/386943d90e312b8c32f4dca6f53724f18b03b873/validation-and-ai-use.md>

### Post-run result — complete only after the pre-run commit

- **Run date and time:** _To complete after the changed-input run._
- **Before allocation / return / volatility:** _To complete after the changed-input run._
- **After allocation / return / volatility:** _To complete after the changed-input run._
- **Mandate verdict before and after:** _To complete after the changed-input run._
- **Did the recommendation change?** _To complete after the changed-input run._
- **Why the result matched or differed from the prediction:** _To complete after the changed-input run._
