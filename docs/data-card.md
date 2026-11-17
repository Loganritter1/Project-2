# Data Card: Trailing Historical-Return Signal

| Field | Record |
|---|---|
| Signal | Annualized trailing mean of simple monthly returns for each ETF sleeve |
| Use in decision | Input to the constrained lowest-volatility allocation search |
| Universe | SGOV, VGIT, VCIT, ACWI |
| Source | Yahoo Finance historical adjusted-close data |
| Source route | `lab13 files/download_yahoo_prices.py` records the Yahoo chart endpoint and four tickers used to create the frozen CSV |
| Download/as-of boundary | Downloaded 2026-10-22; monthly price history through 2026-10 |
| Date-label caution | `2026-10-01` is the final Yahoo monthly bucket. Its value was available at the 2026-10-22 download time but may represent a partial month, not a completed October month. |
| Full window | October 2021 through October 2026 |
| Alternate window | Most recent 36 monthly returns |
| Formula | Mean monthly return times 12; sample monthly volatility times square root of 12 |
| Data quality treatment | The frozen CSV has 61 chronological price rows and no blank price cells. `portfolio.py` rejects missing, non-numeric, or non-positive prices rather than imputing them. |
| Adjustments | Yahoo's adjusted-close series is used as supplied; the project does not independently validate vendor adjustment, revision, or corporate-action methodology. |
| Exclusions | The process excludes individual securities, derivatives, leverage, taxes, transaction-level trading data, and live execution data. |
| Licensing/privacy | The file is a small educational snapshot from a public provider; it contains no personal or account data. Yahoo terms and later vendor revisions are outside this project. |
| Availability limitation | The CSV is a frozen downloaded input. It does not prove intraday availability, vendor revision history, or live-trading execution. |
| Decision limitation | The signal is historical and is not a forecast; it is tested for sensitivity rather than treated as a guarantee. |
