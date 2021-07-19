## Python for Stock Market Analysis

This is a compendium of different Python scripts that I'm developing in order to optimize my investments, and options trading. There's several types of scripts, the naming convention `finance_` generally will pull data from Yahoo Finance, so nothing else is required. The ones named `ibkr_` are based on an Interactive Brokers API implementation and will require that you have an account with the broker, as well as the TWS API installed in your system.

- finance_calculate_rsi.py : Calculates the RSI from a list of stocks and returns its signal ( neutral, oversold, or overbought ) using Yahoo Finance data.
- finance_calculate_ema100.py: Calculates the Exponential Moving Average for the last 100 sessions using Yahoo Finance data.
- ibkr_calculate_ema100.py : Calculates the Exponential Moving Average for the last 100 sessions using the TWS API ( Interactive Brokers ).
- ios_calc_rsi.py : This is the back-end for the iOS app "TA Signals" here: https://github.com/iamgabrielma/TA-Signals
