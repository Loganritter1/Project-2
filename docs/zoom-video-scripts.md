# Zoom Recording Guide and Video Scripts

Use Zoom's **Share Screen** feature and keep a small webcam tile visible. Before recording, open the repository, Streamlit app, and `output/visible-output.md` in separate windows. Record each video separately, then upload each file to YouTube as **Unlisted** with captions enabled.

## Before every recording

1. Close private tabs, notifications, passwords, and personal files.
2. Turn on your webcam and microphone.
3. Share only the required window or browser tab.
4. Say the following disclosure in the first 20 seconds:

> I used OpenAI Codex, based on GPT-5, to help explain requirements, plan and improve the app, improve Streamlit code, and improve presentation. I reviewed the calculations, selected the inputs and process, and the analysis and decision are mine. This is for education only and is not investment advice.

Do not read every document word-for-word. Explain the decision, show the evidence, and use the numbers on screen.

## Video 1: System and thinking changed

**Target length:** 2:30 to 2:50.  
**Share:** `docs/validation-and-ai-use.md`, `docs/data-card.md`, and `output/visible-output.md`.

### Script

**0:00–0:20 — Disclosure**

Read the disclosure above.

**0:20–0:45 — Decision and starting position**

> I am analyzing a constrained portfolio process for the Meridian Foundation Reserve CIO. My conclusion is pilot, not adopt. The process selects the lowest-volatility long-only mix that meets a 6.5% return objective and a 3% reserve-eligible minimum, subject to a provisional 10% volatility limit.

Show the decision-scope and data-boundary sections of `validation-and-ai-use.md`.

**0:45–1:20 — What changed in the analysis**

> The important change was that I stopped treating the base allocation as stable. With the full-history data, the model selects 60% SGOV and 40% ACWI. When I lowered ACWI's expected return from 10.87% to 8%, the mix changed to 35% SGOV and 65% ACWI. The volatility rose from 5.99% to 9.65%.

Show the Locked Changed-Input Record and the before/after table in `output/visible-output.md`.

**1:20–1:55 — AI output checked**

> One AI-assisted code claim I checked was that the app should reject an invalid correlation table instead of silently calculating with it. I tested this by changing one correlation cell so the table became asymmetric. The automated test confirmed that the app raises a ValueError. I accepted that implementation only after the test passed. This check supports the calculation guard; it does not validate the return forecast itself.

Show the AI-output-check table and the named test in `tests/test_portfolio.py`.

**1:55–2:30 — Point-in-time limit and action**

> The signal is a trailing historical-return estimate from a frozen Yahoo Finance price file. It is not a forecast. The last 36 months produces 85% SGOV and 15% ACWI, another 25-point allocation change. That instability is why I recommend a non-funded pilot rather than adoption.

Show `docs/data-card.md`, then the window-stress row in the validation record.

**2:30–2:50 — Close**

> The pilot can proceed only as a validation process. Adoption requires a documented live-cost assumption, final policy treatment of liquidity, issuer, and turnover rules, and monitoring of allocation change, volatility, reserve weight, and mandate verdicts.

## Video 2: Code walkthrough

**Target length:** 4:00 to 4:40.  
**Share:** repository folder/VS Code, terminal, and `output/visible-output.md`.

### Script

**0:00–0:20 — Disclosure**

Read the disclosure above.

**0:20–0:50 — Architecture**

> This is a Streamlit application. `app.py` is the interface. `portfolio.py` calculates return, volatility, covariance, reserve weight, and the grid-search allocation. `prices.csv` is the frozen four-ETF input. `run_validation.py` reproduces the evidence, and `tests/test_portfolio.py` protects the core calculations.

Show the repository tree and README map.

**0:50–1:35 — Data flow and finance logic**

> The app loads monthly adjusted-close prices for SGOV, VGIT, VCIT, and ACWI. It calculates simple monthly returns, annualizes the mean and sample volatility, and validates the correlation matrix. The allocation engine tries long-only weights in five-percentage-point increments, keeps the mixes that meet the return and reserve rules, and selects the lowest-volatility eligible mix.

Show `estimate_from_prices`, `validate_correlations`, and `lowest_risk_mix` in `portfolio.py`.

**1:35–2:15 — App demonstration**

> The interface shows equal weight and inverse volatility beside the 60/40 benchmark and the constrained mix. Every displayed portfolio gets a rule-by-rule verdict for return, reserve, risk, and long-only status. If no eligible mix exists or the proposed mix fails a tested rule, the app stops the process.

Switch to the running Streamlit app. Point to the scorecards and the stop message logic.

**2:15–3:10 — Validation evidence**

> I use a known-answer covariance test: 0.80 times 7% times 6% equals 0.00336. The test suite also checks the base mix, asymmetric-correlation failure, the reserve-constraint stop, and the locked ACWI changed-input direction.

Run and show:

```powershell
python -m unittest discover -s tests -v
```

**3:10–4:00 — Reproduction and limitation**

> Running `python run_validation.py` reproduces the visible base result, the locked changed-input result, the 50-basis-point cost stress, and the 70% reserve failure. The largest limitation is that the cost test is a hurdle analysis rather than an actual trading-cost estimate, and the app does not yet model every liquidity, issuer, and turnover rule.

Run `python run_validation.py` and show `output/visible-output.md`.

**4:00–4:30 — Close**

> A clean clone passed the dependencies, all seven tests, the validation runner, and a headless Streamlit startup. The repository is reproducible, but the financial decision remains pilot rather than adoption because the input estimates and policy terms still need validation.

## Video 3: Committee presentation

**Target length:** 3:30 to 4:30.  
**Share:** Start with the live Streamlit app. Then show `docs/decision-memo.md` and `output/visible-output.md`.

### Script

**0:00–0:20 — Open on the live app and disclosure**

Start with the Streamlit app visible. Read the disclosure above, then say:

> My recommendation is pilot, not adopt.

**0:20–0:55 — Committee decision**

> I recommend that the Meridian Foundation Reserve CIO approve a non-funded pilot of this constrained portfolio process. I am not asking the committee to fund a live allocation today. The purpose of the pilot is to validate the return estimates, cost assumptions, and remaining policy rules.

Point to the proposed portfolio and its verdict in the app.

**0:55–1:35 — Base evidence and comparison**

> In the full-history base case, the constrained mix is 60% SGOV and 40% ACWI. It has a 6.61% gross expected return, 5.99% volatility, and 60% reserve-eligible weight. It passes the current rules. The equal-weight and inverse-volatility baselines are displayed alongside it so the committee can see that the result is not a black-box allocation.

Show the portfolio comparison and risk-return map.

**1:35–2:20 — Why not adopt**

> The process is sensitive to its estimates. In the locked changed-input test, lowering ACWI's expected return to 8% changed the allocation to 35% SGOV and 65% ACWI. Volatility increased to 9.65%, still inside the 10% limit, but the 25-point allocation change means the base mix is not stable enough for adoption.

Show the scenario comparison or `output/visible-output.md`.

**2:20–3:00 — Failure conditions**

> Two additional checks limit the recommendation. With a 50-basis-point annual cost drag, the gross return hurdle rises to 7%, changing the result to 50% SGOV and 50% ACWI. With a 70% reserve requirement, no eligible portfolio can meet the 6.5% objective, and the process stops. The correct behavior is to stop, not to force an allocation.

Show the stress table.

**3:00–3:45 — Ask, monitoring, and reversal**

> My committee ask is approval for a non-funded pilot only. Monitor allocation changes, expected return, annual volatility, reserve-eligible weight, and mandate verdicts whenever the data window, expected return, reserve rule, or cost assumption changes. Stop the process if no long-only mix meets the return and reserve rules, a tested rule fails, or implementation costs make the process infeasible. Adoption requires live cost evidence and final treatment of liquidity, issuer, and turnover constraints.

End on the decision memo's recommendation and monitoring section.

## After recording

1. Watch each video once and correct captions for tickers, `SGOV`, `ACWI`, percentages, and the committee recommendation.
2. Save the corrected transcript as `docs/transcript-video-1.txt`, `docs/transcript-video-2.txt`, and `docs/transcript-video-3.txt`.
3. Replace each `TO ADD AFTER RECORDING` cell in `docs/submission-manifest.csv` with the unlisted YouTube link, exact duration, and timestamp index.
4. Confirm a logged-out browser can open every unlisted YouTube link.
