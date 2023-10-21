FROM python:3.10.6-slim

COPY joke_machine.py . 
COPY requirements.txt .

RUN pip install -r requirements.txt

CMD ["python", "-u", "./joke_machine.py", "-n",  "3"]