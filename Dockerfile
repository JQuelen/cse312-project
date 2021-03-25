FROM python:3.8

#ENV HOME /root
WORKDIR /app

COPY requirements.txt requirements.txt

RUN pip3 install -r requirements.txt

COPY . .

EXPOSE 5000

RUN export FLASK_DEBUG=1
CMD ["python", "-m", "flask", "run", "--host=0.0.0.0"]