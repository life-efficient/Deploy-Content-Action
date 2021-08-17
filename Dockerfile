FROM python:3.8

COPY action.py /action.py
COPY requirements.txt requirements.txt
COPY utils.py utils.py

RUN python -m pip install --upgrade pip \
    pip install -r requirements.txt 

ENTRYPOINT ["python", "/action.py"]