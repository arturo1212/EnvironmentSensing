FROM python:3.4-alpine
COPY . /app
WORKDIR /app
RUN pip install -r ./requirements.txt
ENTRYPOINT ["python"]
CMD ["store_agent.py"]