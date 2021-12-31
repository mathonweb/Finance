# Finance

![Python Versions](https://img.shields.io/pypi/pyversions/pandas)
![Worfklow build](https://circleci.com/gh/mathonweb/Finance/tree/master.svg?style=svg)
![Last Commit](https://img.shields.io/github/last-commit/mathonweb/Finance)
![License](https://img.shields.io/pypi/l/yfinance)
![Repo watchers](https://img.shields.io/github/watchers/mathonweb/Finance?style=social)


## Description
Reports Annual returns from transactions file

## Prerequisite
- Python 3.8
- S3 bucket
- CSV File for transactions formatted like:

| Ticker | Date       | Price | Quantity | Commission |
|--------|------------|-------|----------|------------|
| VUS.TO | 2012-05-16 | 33.36 | 100      | 6.99       |
| XIC.TO | 2014-07-13 | 20.06 | 50       | 6.99       |
| AC.TO  | 2020-11-24 | 23.17 | 200      | 6.99       |


## Configuration
- Edit config.py file to specify 
  - Transaction file (transactions_file)
  - S3 bucket name (bucket_name)
  - Annual returns file (annual_returns_file)

## Outcome
- Txt file with Annual returns (annual_returns_file)
- Log file (logs_file)

## Local execution procedure
- Run python3 finance.py
