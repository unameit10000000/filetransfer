FROM python:latest

ENV PYTHONUNBUFFERED 1
ENV APP_ROOT=/app
ENV FLASK_APP=run.py

# ----------------------
# Filebase env variables
# ----------------------
# WARNING: it's not recommended to create images and deployments using your access keys -
# inside a Dockerfile, instead modify the code and add it to a secured database instance.
ENV FB_ACCESS_KEY="<your-access-key>"
ENV FB_ACCESS_KEY_SECRET="<your-access-key-secret>"
ENV FB_API_ENDPOINT="https://s3.filebase.com"
# ENV FB_DEFAULT_BUCKET="my-default-bucket-name-123"

# -------------------
# Other env variables
# -------------------
ENV APPLICATION_HOST="localhost"
# NOTE: Also change ports at CMD and docker-compose.yml
ENV APPLICATION_PORT=5006
ENV MYSQL_PORT=3306


WORKDIR /app
COPY . ./
RUN pip install -r requirements.txt

CMD [ "python3", "-m" , "flask", "run", "--host=0.0.0.0", "--port=5006" ]
