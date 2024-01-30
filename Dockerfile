FROM python:3.12-alpine
EXPOSE 8123
WORKDIR /app
COPY requirements.txt /app/requirements.txt
RUN pip install --no-cache-dir -r /app/requirements.txt
COPY templates/ /app/templates
COPY yaas.py /app/main.py
CMD ["uvicorn", "main:app", "--host", "0.0.0.0", "--port", "8123"]
