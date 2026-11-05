import csv
import os
from datetime import datetime
from decimal import Decimal, InvalidOperation

DATASET_FILE = "S&P_500Ticker_Dataset.csv"
OUTPUT_FILE = "portfolio_summary.csv"


def load_valid_tickers(filename=DATASET_FILE):
            # Load ticker symbols and company names from a CSV file.
    tickers = {}

    try:
        with open(filename, "r", newline="", encoding="utf-8-sig") as file:
            # Read a small sample to detect common delimiters.
            sample = file.read(4096)
            file.seek(0)

            try:
                dialect = csv.Sniffer().sniff(sample, delimiters=",;\t|")
                reader = csv.DictReader(file, dialect=dialect)
            except csv.Error:
                reader = csv.DictReader(file)

            if not reader.fieldnames:
                print(f"ERROR: '{filename}' is empty or has no header row.")
                return {}

            # Normalize header names: remove spaces/BOM and ignore capitalization.
            original_headers = reader.fieldnames
            normalized_headers = {
                str(header).strip().lstrip("\ufeff").lower(): header
                for header in original_headers
                if header is not None
            }

            symbol_column = None
            for possible_name in (
                "symbol", "ticker", "ticker symbol", "stock symbol",
                "ticker_symbol", "stock_ticker"
            ):
                if possible_name in normalized_headers:
                    symbol_column = normalized_headers[possible_name]
                    break

            company_column = None
            for possible_name in (
                "security", "company", "company name", "name",
                "company_name", "security name"
            ):
                if possible_name in normalized_headers:
                    company_column = normalized_headers[possible_name]
                    break

            if symbol_column is None:
                print("\nERROR: Could not find a ticker/symbol column.")
                print("Columns found in the CSV:", original_headers)
                print("Expected a column named Symbol, Ticker, or Ticker Symbol.")
                print(f"Check that '{filename}' is the correct dataset.")
                return {}

            for row in reader:
                # DictReader keys match the original header strings.
                symbol = str(row.get(symbol_column) or "").strip().upper()
                company = (
                    str(row.get(company_column) or "").strip()
                    if company_column else symbol
                )

                if symbol:
                    tickers[symbol] = company or symbol

        if not tickers:
            print(f"WARNING: No ticker symbols were found in '{filename}'.")
        else:
            print(f"Successfully loaded {len(tickers)} ticker symbols.")
        return tickers

    except FileNotFoundError:
        print(f"\nERROR: Dataset file '{filename}' was not found.")
        print("Keep sp500_constituents.csv in the same folder as portfolio.py.")
        print(f"Current working folder: {os.getcwd()}")
        return {}
    except (OSError, csv.Error) as error:
        print(f"\nERROR: Could not read the dataset: {error}")
        return {}


def read_decimal(prompt, minimum=None):
    # Read a valid decimal number from the console.
    while True:
        raw = input(prompt).strip().replace(",", "")
        try:
            value = Decimal(raw)
            if not value.is_finite():
                raise InvalidOperation
            if minimum is not None and value < minimum:
                print(f"Enter a value greater than or equal to {minimum}.")
                continue
            return value
        except (InvalidOperation, ValueError):
            print("Invalid number. Enter a number such as 125.50.")


def fetch_live_price(symbol):
    # Try to fetch a recent price using yfinance; return None on failure.
    try:
        import yfinance as yf

        ticker = yf.Ticker(symbol)
        price = ticker.fast_info.get("lastPrice")

        if price is None:
            history = ticker.history(period="5d")
            if not history.empty:
                close_prices = history["Close"].dropna()
                if not close_prices.empty:
                    price = close_prices.iloc[-1]

        if price is None:
            return None

        result = Decimal(str(price))
        return result if result > 0 else None
    except Exception:
        return None


def get_current_price(symbol):
    # Automatically retrieve the latest available price; ask manually if unavailable.
    price = fetch_live_price(symbol)

    if price is not None:
        # Print only the retrieved numeric price, with no label or extra message.
        print(f"{price:.2f}")
        return price

    return read_decimal(
        f"Enter current price for {symbol} ($): ", Decimal("0.01")
    )


def money(value):
    """Format a decimal value as currency."""
    return f"${value:,.2f}"


def add_holding(tickers, holdings):
    # Ask for holding details, calculate performance, and store the holding.
    symbol = input("\nEnter stock ticker symbol: ").strip().upper()

    if not symbol:
        print("Ticker symbol cannot be empty.")
        return

    if symbol not in tickers:
        print(f"'{symbol}' was not found in the supplied ticker dataset.")
        print("Check the symbol and try again.")
        return

    company = tickers[symbol]
    print(f"Selected company: {company}")

    buy_price = read_decimal(
        "Enter purchase price per share ($): ", Decimal("0.01")
    )
    shares = read_decimal(
        "Enter number of shares (decimals allowed): ", Decimal("0.000001")
    )
    current_price = get_current_price(symbol)

    invested = buy_price * shares
    market_value = current_price * shares
    gain_loss = market_value - invested
    percentage = (gain_loss / invested) * Decimal("100")

    holding = {
        "symbol": symbol,
        "company": company,
        "buy_price": buy_price,
        "shares": shares,
        "current_price": current_price,
        "invested": invested,
        "market_value": market_value,
        "gain_loss": gain_loss,
        "gain_loss_percent": percentage,
    }
    holdings.append(holding)

    print(f"\nAdded {symbol} - {company}")
    print(f"Invested: {money(invested)}")
    print(f"Market value: {money(market_value)}")
    print(f"Gain/Loss: {money(gain_loss)} ({percentage:+.2f}%)")


def show_portfolio(holdings):
    # Display all holdings and total portfolio performance.
    if not holdings:
        print("\nYour portfolio is empty. Choose option 1 to add a holding.")
        return

    print("\n" + "=" * 112)
    print("STOCK PORTFOLIO PERFORMANCE")
    print("=" * 112)
    print(
        f"{'Ticker':<9}{'Company':<25}{'Shares':>10}"
        f"{'Buy Price':>13}{'Current':>13}{'Invested':>14}"
        f"{'Market Value':>16}{'Gain/Loss':>14}"
    )
    print("-" * 112)

    for item in holdings:
        company = item["company"][:23]
        print(
            f"{item['symbol']:<9}{company:<25}{item['shares']:>10.3f}"
            f"{money(item['buy_price']):>13}{money(item['current_price']):>13}"
            f"{money(item['invested']):>14}{money(item['market_value']):>16}"
            f"{money(item['gain_loss']):>14}"
        )

    total_invested = sum((item["invested"] for item in holdings), Decimal("0"))
    total_value = sum((item["market_value"] for item in holdings), Decimal("0"))
    total_gain = total_value - total_invested
    total_percent = total_gain / total_invested * Decimal("100")

    print("-" * 112)
    print(f"Total invested:     {money(total_invested)}")
    print(f"Total market value: {money(total_value)}")
    print(f"Total gain/loss:    {money(total_gain)} ({total_percent:+.2f}%)")
    print("=" * 112)


def save_summary(holdings, filename=OUTPUT_FILE):
    # Save holdings and a portfolio total row to a CSV report.
    if not holdings:
        print("No holdings to save. Add a stock first.")
        return False

    fields = [
        "Generated_At",
        "Ticker",
        "Company",
        "Buy_Price_USD",
        "Shares",
        "Current_Price_USD",
        "Invested_USD",
        "Market_Value_USD",
        "Gain_Loss_USD",
        "Gain_Loss_Percent",
    ]

    timestamp = datetime.now().astimezone().isoformat(timespec="seconds")
    total_invested = sum((item["invested"] for item in holdings), Decimal("0"))
    total_value = sum((item["market_value"] for item in holdings), Decimal("0"))
    total_gain = total_value - total_invested
    total_percent = total_gain / total_invested * Decimal("100")

    try:
        with open(filename, "w", newline="", encoding="utf-8") as file:
            writer = csv.DictWriter(file, fieldnames=fields)
            writer.writeheader()

            for item in holdings:
                writer.writerow({
                    "Generated_At": timestamp,
                    "Ticker": item["symbol"],
                    "Company": item["company"],
                    "Buy_Price_USD": f"{item['buy_price']:.2f}",
                    "Shares": f"{item['shares']:.6f}".rstrip("0").rstrip("."),
                    "Current_Price_USD": f"{item['current_price']:.2f}",
                    "Invested_USD": f"{item['invested']:.2f}",
                    "Market_Value_USD": f"{item['market_value']:.2f}",
                    "Gain_Loss_USD": f"{item['gain_loss']:.2f}",
                    "Gain_Loss_Percent": f"{item['gain_loss_percent']:.2f}",
                })

            writer.writerow({
                "Generated_At": timestamp,
                "Ticker": "TOTAL",
                "Company": "Portfolio Total",
                "Buy_Price_USD": "",
                "Shares": "",
                "Current_Price_USD": "",
                "Invested_USD": f"{total_invested:.2f}",
                "Market_Value_USD": f"{total_value:.2f}",
                "Gain_Loss_USD": f"{total_gain:.2f}",
                "Gain_Loss_Percent": f"{total_percent:.2f}",
            })

        print(f"\nPortfolio summary saved to: {os.path.abspath(filename)}")
        return True

    except OSError as error:
        print(f"Could not save the CSV file: {error}")
        return False


def main():
    # Main menu and program execution.
    print("=" * 58)
    print("       STOCK PORTFOLIO PERFORMANCE TRACKER")
    print("=" * 58)

    tickers = load_valid_tickers()
    if not tickers:
        input("\nFix the dataset issue, then press Enter to exit.")
        return

    holdings = []

    while True:
        print("\nMENU")
        print("1. Add stock holding")
        print("2. View portfolio performance")
        print("3. Save portfolio summary to CSV")
        print("4. Exit")

        choice = input("Choose an option (1-4): ").strip()

        if choice == "1":
            add_holding(tickers, holdings)
        elif choice == "2":
            show_portfolio(holdings)
        elif choice == "3":
            save_summary(holdings)
        elif choice == "4":
            if holdings:
                save_choice = input(
                    "Save portfolio summary before exiting? (y/n): "
                ).strip().lower()
                if save_choice in ("y", "yes"):
                    save_summary(holdings)
            print("Thank you for using Stock Portfolio Performance Tracker.")
            break
        else:
            print("Invalid option. Please choose 1, 2, 3, or 4.")


if __name__ == "__main__":
    main()
