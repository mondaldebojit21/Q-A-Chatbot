FROM python:3.9-slim
WORKDIR  /app
COPY . /app
RUN pip install -r requirements.txt
EXPOSE 3000
CMD ["uvicorn", "app:app", "--host", "0.0.0.0", "--port", "3000"]