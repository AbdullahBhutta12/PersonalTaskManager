# 1️⃣ Python base image
FROM python:3.12-slim

# 2️⃣ Working directory inside container
WORKDIR /app

# 3️⃣ System dependencies (optional but safe)
RUN apt-get update && apt-get install -y \
    build-essential \
    && rm -rf /var/lib/apt/lists/*

# 4️⃣ Copy requirements
COPY requirements.txt .

# 5️⃣ Install Python dependencies
RUN pip install --no-cache-dir -r requirements.txt

# 6️⃣ Copy full project
COPY . .

# 7️⃣ Expose port (FastAPI default)
EXPOSE 8000

# 8️⃣ Run FastAPI app
CMD ["uvicorn", "main:app", "--host", "0.0.0.0", "--port", "8000"]