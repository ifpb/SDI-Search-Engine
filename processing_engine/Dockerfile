FROM python:3

COPY . .

COPY requirements.txt .

RUN pip3 install --no-cache-dir -r requirements.txt

CMD ["python", "main.py"]