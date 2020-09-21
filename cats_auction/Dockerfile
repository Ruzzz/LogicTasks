FROM python:3.7
WORKDIR /usr/src/app
COPY . .
RUN pip install -r requirements.txt
RUN pip install alembic
ENV CATSAUCTION_CONF "prod"
CMD make db-migrate && python -m catsauction.wsgi
