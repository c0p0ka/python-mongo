FROM python:3.7-alpine
ADD . /webapp
WORKDIR /webapp
RUN pip install -r requirements.txt
CMD python app.py