FROM python:3.8-slim-buster

WORKDIR /usr/src/app

RUN apt-get update
RUN apt-get install -y wkhtmltopdf

COPY requirements.txt ./
COPY config.ini ./
COPY execution.sh ./
COPY finance/finance.py ./
COPY finance/report.py ./
COPY finance/historical_utils.py ./
COPY finance/portfolio_utils.py ./
COPY finance/transactions_utils.py ./
COPY finance/utils/errors_finder.py ./utils/
COPY finance/utils/logger.py ./utils/
COPY finance/utils/s3_client.py ./utils/

RUN pip install --no-cache-dir -r requirements.txt

CMD sh execution.sh