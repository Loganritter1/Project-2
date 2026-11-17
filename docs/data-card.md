# Data Card: Trailing Historical-Return Signal

| Field | Record |
|---|---|
| Signal | Annualized trailing mean of simple monthly returns for each ETF sleeve |
| Use in decision | Input to the constrained lowest-volatility allocation search |
| Universe | SGOV, VGIT, VCIT, ACWI |
| Source | Yahoo Finance historical adjusted-close data |
| Download/as-of boundary | Downloaded 2026-10-22; monthly price history through 2026-10 |
| Full window | October 2021 through October 2026 |
| Alternate window | Most recent 36 monthly returns |
| Formula | Mean monthly return times 12; sample monthly volatility times square root of 12 |
| Availability limitation | The CSV is a frozen downloaded input. It does not prove intraday availability, vendor revision history, or live-trading execution. |
| Decision limitation | The signal is historical and is not a forecast; it is tested for sensitivity rather than treated as a guarantee. |
