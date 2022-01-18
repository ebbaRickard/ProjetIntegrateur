FROM python:3.9



COPY ./requirements.txt /app/

COPY ./app /app/src

WORKDIR /app

RUN pip install -r requirements.txt

EXPOSE 8000

CMD ["uvicorn", "src.main:app", "--host=0.0.0.0", "--reload"]
