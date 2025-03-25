FROM python:3.9-alpine

WORKDIR /sqs_puller

COPY requirements.txt .

RUN pip install --no-cache-dir -r requirements.txt

RUN pip install pytest

COPY . .

CMD ls

ENV AWS_ACCESS_KEY=
ENV AWS_SECRET_KEY=
ENV AWS_REGION=
ENV SQS_QUEUE_URL=
ENV S3_BUCKET=
ENV SQS_MSGS_FILE=
ENV WAIT_TIME_SECONDS=10

CMD [ "python", "sqs_puller.py" ]

