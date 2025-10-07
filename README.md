# Sirius Email Service

Servicio de email con autenticación JWT y sistema interactivo por terminal.

## Configuración Local

### 1. Crear entorno virtual
```bash
python3 -m venv venv
source venv/bin/activate  
```

### 2. Instalar dependencias
```bash
pip install -r requirements.txt
```

### 3. Ejecutar la aplicación
```bash
python app.py
```

## Ejecución con Docker

### Terminal 1: Servicios en Docker
```bash
docker-compose up --build
```

Para detener los servicios:
```bash
docker-compose down
```

### Terminal 2: Servicio interactivo directo
```bash
newgrp docker
docker exec -it sirius-email-service bash
python app.py
```

## Tests

```bash
./run_simple_tests.sh
```


## Estructura del Proyecto
```
├── app.py              # Aplicación principal
├── email_service.py    # Servicio de email
├── requirements.txt    # Dependencias de Python
├── Dockerfile         # Configuración de Docker
├── docker-compose.yml # Orquestación de servicios
└── README.md          # Este archivo
```