FROM python:3.9.2-slim
ARG APP_VERSION=dev-local
ENV APP_VERSION=${APP_VERSION}
WORKDIR /opt
COPY . /opt
RUN pip install --no-cache-dir -r /opt/dependencias.txt
EXPOSE 8080
CMD ["python3", "/opt/app.py"]
