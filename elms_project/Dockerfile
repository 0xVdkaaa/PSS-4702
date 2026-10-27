# Pake image Python resmi yang ringan
FROM python:3.11-slim

# Biar log error Python langsung muncul di terminal
ENV PYTHONUNBUFFERED=1

# Bikin folder kerja di dalam Docker
WORKDIR /app

# Copy file requirements dan install
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Copy semua file project lu ke dalam Docker
COPY . .

# Buka port 8000
EXPOSE 8000