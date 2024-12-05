FROM python:3.12

ADD . .
RUN apt-get -y update
RUN apt-get -y upgrade
RUN apt-get install -y ffmpeg
RUN mkdir /songs
RUN pip install -r ./requirements.txt

CMD ["python", "./main.py"]
