# Stock Portfolio Performance Tracker

## Project Overview

The Stock Portfolio Performance Tracker is a Python-based console application designed to manage and monitor stock investments. It allows users to select stock ticker symbols from an S&P 500 constituents CSV dataset, enter purchase prices and share quantities, and automatically retrieve the latest available stock prices using Yahoo Finance.

The application calculates individual stock performance, total invested capital, current market value, profit or loss, and percentage returns. It also generates an external CSV report containing all portfolio holdings and overall portfolio performance.

 ## Project Objectives

- Load stock ticker symbols and company names from a CSV dataset.
- Validate stock symbols before accepting investment details.
- Retrieve recent stock prices using Yahoo Finance.
- Allow manual price entry when automatic retrieval fails.
- Calculate invested capital and current market value.
- Calculate individual stock profit and loss.
- Calculate percentage gain or loss.
- Display portfolio performance through a menu-driven interface.
- Export portfolio details and total performance into a CSV file.

## Technologies Used
Python 3| Main programming language

CSV Module| Reading and writing CSV files

OS Module| File and directory management

Warnings Module| Suppressing unnecessary warnings

Datetime Module| Generating date and time

Decimal Module| Accurate financial calculations

yfinance| Retrieving stock market prices

Yahoo Finance| External stock market data source

## Project Folder Structure
```
Stock-Portfolio-Tracker/
├── portfolio.py
├── S&P_500Ticker_Dataset.csv
├── portfolio_summary.csv
└── README.md
```
File Description

1) portfolio.py: Main Python application containing all program functions.
2) constituents.csv: Input dataset containing stock ticker symbols and company names.
3) portfolio_summary.csv: Automatically generated portfolio performance report.
4) README.md: Project documentation.


## Dataset Description

The project uses an S&P 500 constituents CSV dataset containing company names and their corresponding stock ticker symbols.

Example:

Symbol,Security

AAPL,Apple Inc.

AMZN,Amazon.com Inc.

GOOGL,Alphabet Inc.


## Installation and Setup

Step 1: Install Python

Install Python 3 and verify the installation:

 ```cmd
  python --version 
```

Step 2: Open the project in VS Code

Open the project folder containing "portfolio.py" and "S&P_500Ticker_Dataset".



Step 3: Install the required library

Open the VS Code terminal and execute:
 ```cmd
python -m pip install yfinance
```

Step 4: Run the application

Execute the following command:
``` cmd
python portfolio.py
```
5. Application Workflow

### The application follows these steps:

1. Start the Python application.
2. Load the S&P 500 ticker dataset.
3. Validate the dataset headers and ticker symbols.
4. Display the main menu.
5. Allow the user to add stock holdings.
6. Accept purchase price and share quantity.
7. Retrieve the latest available stock price.
8. Calculate investment value and profit/loss.
9. Display portfolio performance.
10. Generate the portfolio summary CSV file.


## Overall Portfolio Performance

Total Invested = Sum of all invested values

Total Market Value = Sum of all current market values

Total Gain/Loss = Total Market Value − Total Invested

Overall Return % = (Total Gain/Loss / Total Invested) × 100

## Live Stock Price Retrieval

1.The project uses the "yfinance" Python library to retrieve recent stock market prices.

First, the program attempts to retrieve the latest price using:
ticker.fast_info.get("lastPrice")

2.If the price is unavailable, the application checks recent historical closing prices:

ticker.history(period="5d")


3.If both methods fail, the application requests manual current-price input.


4.This ensures that users can continue tracking their portfolio even when online price retrieval is unavailable.

Note: Yahoo Finance prices may be delayed and are not guaranteed to represent real-time exchange prices.

## CSV Report Generation

The application automatically creates an external file named:
            
```
portfolio_summary.csv
```

## Limitations

- Stock prices depend on Yahoo Finance data availability.
- Market prices may be delayed.
- Previously saved portfolios are not automatically loaded when restarting the application.
- Saving the report overwrites the previous CSV report.
- Brokerage charges, taxes, and dividends are not included.
- Currency conversion is not supported.
- The application is designed for educational purposes and does not provide investment advice.

## Future Enhancements

The project can be extended with the following features:

- Interactive dashboard using Streamlit.
- Historical stock price visualization.
- Portfolio allocation pie charts.
- Stock price alerts and notifications.
- Database integration using MySQL.
- Downloadable PDF portfolio reports.
