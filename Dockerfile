FROM django:python2
MAINTAINER Ryan Grieve<me@ryangrieve>

ENV PYTHONUNBUFFERED 1

ADD requirements.txt /tmp/requirements.txt
RUN pip install -r /tmp/requirements.txt

ADD . /app
WORKDIR /app

CMD ["python", "manage.py", "runserver"]

EXPOSE 8000
