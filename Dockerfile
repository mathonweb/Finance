FROM python:3.8-slim-buster

WORKDIR /usr/src/app

COPY requirements.txt ./
COPY config.py ./
COPY finance_utils.py ./
COPY historical_utils.py ./
COPY portfolio_utils.py ./
COPY transactions_utils.py ./
COPY utils/errors_finder.py ./utils/errors_finder.py
COPY utils/logger.py ./utils/logger.py
COPY transactions/transactions.csv ./transactions/
COPY transactions/Historical_data/ ./transactions/Historical_data/

RUN pip install --no-cache-dir -r requirements.txt

CMD python finance_utils.py