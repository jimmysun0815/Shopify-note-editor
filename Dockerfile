FROM python:3.9

ADD requirements.txt requirements.txt
RUN pip3 install -r requirements.txt

WORKDIR /app
ADD *.py ./

CMD python3 -u app.py