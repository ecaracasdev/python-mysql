# NOTE name need to be Dockerfile
FROM python:3.9

RUN pip install mysql-connector-python
RUN pip install flask
RUN pip install -U Flask-SQLAlchemy
RUN pip install mysqlclient
RUN pip install flask-login

WORKDIR /usr/app/src

COPY ./ ./

CMD ["python", "index.py"]