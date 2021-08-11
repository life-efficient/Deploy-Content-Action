FROM python:3.8

COPY action.py /action.py
COPY requirements.txt requirements.txt

RUN python -m pip install --upgrade pip \
    pip install -r requirements.txt 

ENTRYPOINT ["python", "/action.py"]