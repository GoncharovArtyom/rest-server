FROM python:3.6

EXPOSE 65432

COPY . /bin/server
WORKDIR /bin/server

RUN pip install pipenv && pipenv install --system

CMD ["python", "run_server.py"]
