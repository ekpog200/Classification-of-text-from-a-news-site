FROM python:3.11

WORKDIR /workdir
COPY requirements.txt model_prediction.py utils.py /workdir/


RUN pip install -r requirements.txt

ENV BACKEND_URI sqlite:///mlflow.db

EXPOSE 5000

CMD mlflow ui --backend-store-uri $BACKEND_URI --host 0.0.0.0