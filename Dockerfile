FROM python:3.9-slim-buster
 
WORKDIR /app
 
COPY requirements.txt .
RUN python -m pip install --upgrade pip
RUN python -m pip install -r requirements.txt
 
COPY . .
 
EXPOSE 8000
CMD ["python3", "manage.py", "runserver", "0.0.0.0:8000"]