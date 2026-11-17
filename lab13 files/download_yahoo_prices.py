"""Download monthly adjusted-close history for the Lab 15 ETF universe from Yahoo Finance."""

import csv
import json
from datetime import datetime, timezone
from urllib.request import Request, urlopen


TICKERS = ("SGOV", "VGIT", "VCIT", "ACWI")
START_UNIX = 1633046400  # 2021-10-01 UTC
END_UNIX = 1792713600  # 2026-10-23 UTC


def monthly_adjusted_closes(ticker):
    """Return {YYYY-MM-01: adjusted close} for one Yahoo Finance ticker."""
    url = (
        f"https://query1.finance.yahoo.com/v8/finance/chart/{ticker}"
        f"?period1={START_UNIX}&period2={END_UNIX}&interval=1mo"
        "&events=history&includeAdjustedClose=true"
    )
    request = Request(url, headers={"User-Agent": "Mozilla/5.0"})
    with urlopen(request) as response:
        data = json.load(response)
    result = data["chart"]["result"][0]
    closes = result["indicators"]["adjclose"][0]["adjclose"]
    return {
        datetime.fromtimestamp(timestamp, timezone.utc).strftime("%Y-%m-01"): close
        for timestamp, close in zip(result["timestamp"], closes)
        if close is not None
    }


def main():
    """Write common monthly observations in chronological order to prices.csv."""
    data = {ticker: monthly_adjusted_closes(ticker) for ticker in TICKERS}
    common_months = sorted(set.intersection(*(set(values) for values in data.values())))
    with open("prices.csv", "w", newline="", encoding="utf-8") as output_file:
        writer = csv.writer(output_file)
        writer.writerow(("Date", *TICKERS))
        for month in common_months:
            writer.writerow((month, *(data[ticker][month] for ticker in TICKERS)))
    print(f"Wrote {len(common_months)} monthly observations to prices.csv.")


if __name__ == "__main__":
    main()
