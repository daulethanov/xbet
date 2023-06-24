FROM python:3.11
RUN pip install pipenv

WORKDIR /backend

COPY Pipfile Pipfile.lock ./

RUN pipenv install --dev --system --deploy

COPY . .

CMD gunicorn --bind 0.0.0.0:5000 app:app



