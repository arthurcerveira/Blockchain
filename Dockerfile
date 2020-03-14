FROM python:3 

WORKDIR usr/src/app

# We copy just the requirements.txt first to leverage
COPY requirements.txt .
RUN pip install -r requirements.txt

COPY . .

ENTRYPOINT [ "python" ]

CMD [ "network.py" ]

