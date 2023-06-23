FROM python:latest

ENV PYTHONUNBUFFERED=1


WORKDIR /usr/src/app

COPY . .

RUN pip install -r requirements.txt

EXPOSE 5000

CMD ["python", "app.py"]