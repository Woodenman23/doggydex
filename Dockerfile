# Build stage
FROM python:3.12-slim AS builder
WORKDIR /app
COPY requirements.txt .
# Install system dependencies
RUN apt-get update && apt-get install -y --no-install-recommends \
    libglib2.0-0 \
    libpng16-16 \
    && rm -rf /var/lib/apt/lists/*
# Install non-PyTorch dependencies from PyPI
RUN pip install --no-cache-dir --user \
    gunicorn==22.0.0 \
    Flask==3.0.3 \
    pillow==10.4.0 \
    google-auth==2.34.0 \
    google-api-python-client==2.149.0
# Install PyTorch dependencies from PyTorch index
RUN pip install --no-cache-dir --user \
    torch==2.3.1 \
    torchvision==0.18.1 \
    --index-url https://download.pytorch.org/whl/cpu

# Runtime stage
FROM python:3.12-slim
WORKDIR /app
# Install runtime system dependencies
RUN apt-get update && apt-get install -y --no-install-recommends \
    libglib2.0-0 \
    libpng16-16 \
    && rm -rf /var/lib/apt/lists/*
# Copy Python packages and binaries
COPY --from=builder /root/.local/lib/python3.12/site-packages /usr/local/lib/python3.12/site-packages
COPY --from=builder /root/.local/bin /usr/local/bin
# Copy app files
COPY . .
COPY secrets/doggydex-456203-e6ca832dbc3c.json ./secrets/
EXPOSE 8080
ENV BASE_PATH=/doggydex
# RUN python3 download_weights.py
CMD ["gunicorn", "-b", "0.0.0.0:8080", "app:app"]