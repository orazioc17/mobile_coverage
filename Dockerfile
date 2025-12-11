# Imagen base ligera
FROM python:3.14-slim

ENV PYTHONDONTWRITEBYTECODE 1
ENV PYTHONUNBUFFERED 1

# Directorio de trabajo (raíz del proyecto)
WORKDIR /app

# Copiar requirements e instalar
COPY requirements.txt /app/
RUN pip install --upgrade pip
RUN pip install -r requirements.txt

# Copiar todo el proyecto
COPY . /app/

# Exponer puerto
EXPOSE 8000

# CMD apuntando a la ruta real de manage.py
CMD ["python", "mobile_coverage/manage.py", "runserver", "0.0.0.0:8000"]