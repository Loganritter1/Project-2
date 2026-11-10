# Meridian Portfolio Stability Decision

This Project 2 app helps the Meridian Foundation Reserve CIO evaluate a long-only portfolio that meets a 6.5% annual expected-return objective while maintaining at least 3% in reserve-eligible Treasury assets. It selects the lowest-volatility allocation among portfolios tested in 5-percentage-point increments.

**Decision:** Pilot rather than adopt. The recommended allocation changes when the return assumptions and the historical sample change. Adopt only after validating the return assumptions and explaining the large allocation change between the full sample and the most recent 36 months.

## Run the app

From this folder, run:

```powershell
py -m pip install streamlit; py -m streamlit run ".\lab13 files\app.py"
```

The browser app opens automatically. The result appears under **Lowest-risk mix with your current edits**. Use the sidebar controls or upload `lab13 files/prices.csv` to test a changed input. The adjacent **Answer for inputs as loaded** panel is the comparison result.

## Read the result without running code

The committed result, stress test, data sources, and decision rationale are in [lab13 files/lab15.md](lab13%20files/lab15.md). The decision engine's default training-input baselines and mandate calculations are documented in [lab13 files/lab13.md](lab13%20files/lab13.md).

## Repository map

- `lab13 files/app.py` - Streamlit interface and editable decision controls.
- `lab13 files/portfolio.py` - allocation search, return/volatility calculations, CSV estimation, and input validation.
- `lab13 files/prices.csv` - monthly adjusted-close input data for SGOV, VGIT, VCIT, and ACWI.
- `lab13 files/download_yahoo_prices.py` - data-download helper.
- `lab13 files/lab15.md` - visible results, stress tests, source links, and the final decision rationale.
- `lab13 files/mandate.py` and `lab13 files/lab13.md` - the earlier coded mandate rules and their documentation.

## Input and decision boundary

`prices.csv` contains monthly adjusted-close data downloaded from Yahoo Finance on 2026-10-22. The app converts monthly returns to annual historical estimates; these are estimates, not forecasts. The app is a classroom demonstration and not investment advice.

## Validation and changed-input evidence

`portfolio.py` validates that correlations are within -1 to 1 and symmetric before using them in a covariance matrix. The documented tests in [lab15.md](lab13%20files/lab15.md) include an expected-return stress, a correlation stress, and a comparison between the full history and the most recent 36 monthly returns.
