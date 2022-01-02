FROM python:3.8-slim-buster

WORKDIR /usr/src/app

RUN apt-get update
RUN apt-get install -y wkhtmltopdf

COPY requirements.txt ./
COPY config.py ./config.py
COPY finance.py ./
COPY report.py ./
COPY historical_utils.py ./
COPY portfolio_utils.py ./
COPY transactions_utils.py ./
COPY utils/errors_finder.py ./utils/errors_finder.py
COPY utils/logger.py ./utils/logger.py
COPY utils/s3_client.py ./utils/s3_client.py
COPY execution.sh ./

RUN pip install --no-cache-dir -r requirements.txt

CMD sh execution.sh