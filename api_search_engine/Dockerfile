FROM python:3

WORKDIR /api_search_engine

COPY . .

RUN pip3 install --no-cache-dir -r requeriments.txt

ENTRYPOINT ["python"]

CMD ["app.py"]