FROM python:3.8-slim
WORKDIR /count
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt
COPY . .
EXPOSE 5004
CMD ["python", "count.py"]