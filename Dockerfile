FROM python:3.10-slim
ENV PYTHONUNBUFFERED 1

WORKDIR /app
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt
COPY *.py ./
COPY plugins ./plugins
CMD ["python", "router_monitor.py"]
