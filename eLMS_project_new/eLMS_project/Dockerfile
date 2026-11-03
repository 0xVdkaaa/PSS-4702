# Pake base image Python
FROM python:3.10-slim

# Biar log Python langsung nongol di terminal Docker & ga nyampah file .pyc
ENV PYTHONDONTWRITEBYTECODE=1
ENV PYTHONUNBUFFERED=1

# Set working directory di dalem container
WORKDIR /app

# Copy requirements lu ke dalem container terus install dependencies-nya
COPY requirements.txt /app/
RUN pip install --upgrade pip && pip install -r requirements.txt

# Copy sisa file project lu ke dalem container
COPY . /app/