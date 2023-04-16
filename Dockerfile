FROM python:3.9

LABEL name="cvat-webhook" auth="gwt"

WORKDIR /app

COPY . /app

RUN pip install -r requirements.txt

CMD [ "python", "main.py" ]

RUN echo 'cvat-webhook-flask build completed...'
