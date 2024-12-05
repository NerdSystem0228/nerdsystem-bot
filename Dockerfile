FROM python:3.12

ADD . .

RUN pip install -r ./requirements.txt

CMD ["python", "./main.py"]
