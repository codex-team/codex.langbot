FROM python:3.8.7-slim-buster

WORKDIR /usr/src/app

COPY requirements.txt .
RUN pip install -r requirements.txt

COPY main.py .
ENTRYPOINT ["python"]
CMD ["main.py"]