FROM python:3.12

COPY . .
RUN apt-get -y update && apt-get -y upgrade && apt-get install -y ffmpeg
RUN mkdir /songs
RUN pip install -r ./requirements.txt
CMD ["python", "./main.py"]
