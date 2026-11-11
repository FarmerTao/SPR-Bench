FROM python:3.12.10-slim
WORKDIR /app
COPY requirements.txt /tmp/requirements.txt
RUN pip install --no-cache-dir -r /tmp/requirements.txt
COPY data /app/data
COPY spec /app/spec
RUN mkdir -p /app/submission /app/output
CMD ["bash"]
