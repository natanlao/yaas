FROM tiangolo/uwsgi-nginx-flask:python3.8-alpine
COPY requirements.txt /app
RUN pip install -r /app/requirements.txt
COPY uwsgi.ini /app
COPY templates/ /app/templates
COPY yaas.py /app