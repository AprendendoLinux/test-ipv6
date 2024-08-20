FROM python:3.9.2-slim
WORKDIR /opt
#COPY app.py static templates dependencias.txt /opt
COPY . /opt
RUN pip install --no-cache-dir -r /opt/dependencias.txt
EXPOSE 8080
CMD ["python3", "/opt/app.py"]
