FROM python:latest as BUILD

COPY requirements.txt .
COPY . .

RUN pip install -r requirements.txt

CMD ["python", "app.py"]