# ================================
# ETAPA 1: IMAGEN BASE
# ================================
FROM python:3.11-slim

# ================================
# ETAPA 2: METADATOS
# ================================
LABEL maintainer="tu-email@ejemplo.com"
LABEL description="DevBlog - Aplicación de blog para aprender DevOps"
LABEL version="1.0"

# ================================
# ETAPA 3: CONFIGURACIÓN DE PRODUCCIÓN
# ================================
ENV PYTHONUNBUFFERED=1
ENV PYTHONDONTWRITEBYTECODE=1
ENV FLASK_ENV=production
ENV PORT=5000  
# Usado por Railway

# ================================
# ETAPA 4: INSTALACIÓN DE DEPENDENCIAS
# ================================
WORKDIR /app

# Instalar curl para health checks (requerido por Railway)
RUN apt-get update && apt-get install -y \
    curl \
    && rm -rf /var/lib/apt/lists/*

COPY requirements.txt .

RUN pip install --no-cache-dir --upgrade pip && \
    pip install --no-cache-dir -r requirements.txt

# ================================
# ETAPA 5: COPIAR CÓDIGO
# ================================
COPY . .

# ================================
# ETAPA 6: CONFIGURACIÓN DE SEGURIDAD
# ================================
RUN adduser --disabled-password --gecos '' appuser && \
    chown -R appuser:appuser /app
USER appuser

# ================================
# ETAPA 7: HEALTH CHECK (REQUERIDO POR RAILWAY)
# ================================
HEALTHCHECK --interval=30s --timeout=30s --start-period=5s --retries=3 \
    CMD curl -f http://localhost:$PORT/api/health || exit 1

# ================================
# ETAPA 8: CONFIGURACIÓN DE RED
# ================================
EXPOSE $PORT

# ================================
# ETAPA 9: COMANDO DE INICIO
# ================================
CMD ["python", "app.py"]