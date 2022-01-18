FROM python:3.8-slim-buster

WORKDIR /usr/src/app

RUN apt-get update
RUN apt-get install -y wkhtmltopdf

RUN export PYTHONPATH="%PYTHONPATH%:/usr/src/app/"

COPY requirements.txt ./
COPY config.ini ./
COPY execution.sh ./
COPY report.py ./
COPY finance/__init__.py ./finance/
COPY finance/__main__.py ./finance/
COPY finance/finance_calc.py ./finance/
COPY finance/historical_utils.py ./finance/
COPY finance/portfolio_utils.py ./finance/
COPY finance/transactions_utils.py ./finance/
COPY finance/utils/__init__.py ./finance/utils/
COPY finance/utils/logger.py ./finance/utils/
COPY finance/utils/s3_client.py ./finance/utils/

RUN pip install --no-cache-dir -r requirements.txt

CMD sh execution.sh