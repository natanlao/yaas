FROM tiangolo/uvicorn-gunicorn-starlette:python3.8-alpine3.10
COPY requirements.txt /app
RUN pip install -r /app/requirements.txt
COPY templates/ /app/templates
COPY yaas.py /app/main.py
