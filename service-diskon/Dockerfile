FROM python:3.10-slim
WORKDIR /app
COPY requirements.txt .
RUN pip install -r requirements.txt
COPY service-diskon/ .
EXPOSE 80
CMD ["python", "app.py"]