FROM python:3.9-alpine

WORKDIR /ms1

COPY requirements.txt .

RUN pip install --no-cache-dir -r requirements.txt

RUN pip install pytest

COPY ms1/ .

CMD [ "python", "ms1.py" ]
