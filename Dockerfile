FROM python:3.8

#ENV HOME /root
WORKDIR /app

COPY requirements.txt requirements.txt

RUN pip3 install -r requirements.txt

COPY . .

EXPOSE 5000

ADD https://github.com/ufoscout/docker-compose-wait/releases/download/2.2.1/wait /wait
RUN chmod +x /wait

RUN export FLASK_DEBUG=1
CMD /wait
CMD /wait && ["python", "-m", "flask", "run", "--host=0.0.0.0"]