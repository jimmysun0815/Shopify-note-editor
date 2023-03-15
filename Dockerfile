FROM python:3.9
  
WORKDIR /app
ADD *.py ./

CMD python3 -u app.py