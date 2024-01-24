FROM python:3.10

RUN mkdir /app
COPY . /app
EXPOSE 5000

WORKDIR /app
RUN pip install --upgrade pip
RUN pip install -r requirements.txt

# Run DB migrations every time
#CMD make db-migrate && make db-upgrade && make run
CMD ["/bin/sh"]
