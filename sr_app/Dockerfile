FROM python:3.9-slim

WORKDIR /sr_app

RUN apt-get update
RUN apt-get install -y vim

COPY requirements.txt requirements.txt
RUN pip3 install -r requirements.txt

COPY gunicorn.conf.py ./

COPY . .

EXPOSE 8000

#CMD [ "gunicorn", "sr_app.wsgi", "--bind", "0.0.0.0:8000"]
CMD [ "python", "manage.py", "runserver", "0.0.0.0:8000"]