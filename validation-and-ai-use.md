# Validation and AI Use

## Scope and validation status

This application compares equal-weight, inverse-volatility, and 60/40 benchmark portfolios with a constrained lowest-risk portfolio. The constrained portfolio is long-only and is tested against an expected-return objective, a reserve-eligible minimum, and a provisional annual-volatility limit.

Completed local checks:

- The app opens with the three comparison portfolios, a benchmark, allocation displays, mandate verdicts, and a risk/return chart.
- With the built-in training assumptions, the constrained mix is 0% Treasury bills / 20% Treasury 10-year note / 25% investment-grade bonds / 55% global equities. Its estimated return is 6.51%, annual volatility is 9.44%, and reserve-eligible allocation is 20%.
- With `lab13 files/prices.csv`, the app recognizes SGOV and VGIT as reserve-eligible. The constrained mix is 60% SGOV / 40% ACWI, with 6.61% estimated return, 5.99% annual volatility, and 60% reserve-eligible allocation.
- Equal-weight and inverse-volatility portfolios are shown beside the constrained portfolio and receive a rule-by-rule mandate verdict.

## Process-stopping condition

Stop the process and do not recommend an allocation if no long-only portfolio can meet the return and reserve requirements, or if the proposed portfolio fails a tested mandate rule. Review the data, assumptions, and mandate before rerunning the process.

## Locked Changed-Input Record

- **Input:** ACWI expected annual return estimate.
- **Old value:** 10.87% per year.
- **New value:** 8.0% per year.
- **Prediction:** Lowering ACWI's expected return from 10.87% to 8.0% will require more ACWI in the constrained mix to reach the 6.5% return objective. I expect annual portfolio volatility to increase. The recommendation may change from pilot to stop/reject if the increased volatility exceeds the 10.0% provisional limit.
- **Prediction written on:** 11/17/2026, 4:00PM
- **Pre-run commit and GitHub link:** 

### Post-run result — complete only after the pre-run commit

- **Run date and time:** _To complete._
- **Before allocation / return / volatility:** _To complete._
- **After allocation / return / volatility:** _To complete._
- **Mandate verdict before and after:** _To complete._
- **Did the recommendation change?** _To complete._
- **Why the result matched or differed from the prediction:** _To complete._

## AI use and authorship

I used AI to help explain course requirements, plan the application structure, improve Streamlit code, and improve the app's visual presentation. I reviewed the resulting code and calculations, selected the inputs and process, and remain responsible for the analysis and decision.

This analysis is for education only and is not investment advice.

