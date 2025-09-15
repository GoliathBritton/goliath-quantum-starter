FROM python:3.11-slim
WORKDIR /app
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt
COPY worker.py .
COPY run_worker.sh .
RUN chmod +x run_worker.sh
CMD ["./run_worker.sh"]