# 📧 Sistema de Email Interactivo Multi-Proveedor# 📧 Sistema de Email Interactivo Multi-Proveedor# 📧 API de Email Multi-Proveedor con JWT# 📧 API de Email Súper Simple



Sistema completo de email con **modo interactivo por terminal**, **registro de usuarios**, **doble redundancia** (SendGrid + Mailgun), autenticación JWT y base de datos Supabase.



## 🚀 Características PrincipalesSistema completo de email con **modo interactivo por terminal** y **doble redundancia** (SendGrid + Mailgun), autenticación JWT y base de datos Supabase.



- ✅ **Registro de usuarios**: Crear cuentas desde terminal

- ✅ **Modo interactivo**: Login y envío por terminal

- ✅ **Doble redundancia**: SendGrid + Mailgun  ## 🚀 Características PrincipalesAPI robusta de email con **doble redundancia** (SendGrid + Mailgun), autenticación JWT y base de datos Supabase.API de email con autenticación JWT **súper fácil de usar**. Sin base de datos, sin Supabase, todo en un archivo.

- ✅ **Fallback automático**: Si un proveedor falla, usa el otro

- ✅ **Selección manual**: Elige qué proveedor usar

- ✅ **Seguridad total**: Solo el email del usuario logueado puede enviar

- ✅ **JWT Authentication**: Tokens con 1 hora de expiración- ✅ **Modo interactivo**: Login y envío por terminal

- ✅ **Base de datos Supabase**: Almacenamiento seguro de usuarios

- ✅ **Arquitectura limpia**: Patrón de proveedores con clases abstractas- ✅ **Doble redundancia**: SendGrid + Mailgun  



## 🛠️ Instalación- ✅ **Fallback automático**: Si un proveedor falla, usa el otro## 🚀 Características Principales## 🚀 Instalación Rápida



1. **Clonar e instalar dependencias:**- ✅ **Selección manual**: Elige qué proveedor usar

```bash

git clone <repo>- ✅ **Seguridad**: Solo el email del usuario logueado puede enviar

cd Sirius-challenge

python -m venv venv- ✅ **JWT Authentication**: Tokens con 1 hora de expiración

source venv/bin/activate  # Linux/Mac

pip install -r requirements.txt- ✅ **Base de datos Supabase**: Almacenamiento seguro de usuarios- ✅ **Doble redundancia**: SendGrid + Mailgun1. **Instalar dependencias:**

```

- ✅ **Arquitectura limpia**: Patrón de proveedores con clases abstractas

2. **Configurar variables de entorno:**

```bash- ✅ **Fallback automático**: Si un proveedor falla, usa el otro```bash

cp .env.example .env

# Editar .env con tus credenciales:## 🛠️ Instalación

# - SENDGRID_API_KEY

# - MAILGUN_API_KEY y MAILGUN_DOMAIN- ✅ **Selección manual**: Elige qué proveedor usarpip install -r requirements_simple.txt

# - SUPABASE_URL y SUPABASE_KEY

```1. **Clonar e instalar dependencias:**



## 🎯 Uso del Sistema```bash- ✅ **JWT Authentication**: Tokens con 1 hora de expiración```



### Modo Interactivo (Principal)git clone <repo>

```bash

# Ejecutar sistema interactivocd Sirius-challenge- ✅ **Base de datos Supabase**: Almacenamiento seguro de usuarios

python app.py

python -m venv venv

# Te pedirá:

# 1. ¿Iniciar sesión o registrarse?source venv/bin/activate  # Linux/Mac- ✅ **Arquitectura limpia**: Patrón de proveedores con clases abstractas2. **Configurar email:**

# 2. Datos del usuario/registro

# 3. Menú principal con opcionespip install -r requirements.txt

```

``````bash

### Modo API (Opcional)

```bash

# Ejecutar como API REST

python app.py --api2. **Configurar variables de entorno:**## 🛠️ Instalacióncp .env_simple .env

```

```bash

## 📱 Flujo de Uso Interactivo

cp .env.example .env# Editar .env y poner tu API key de SendGrid

```

🔐 AUTENTICACIÓN# Editar .env con tus credenciales:

├── 1. Iniciar sesión (si ya tienes cuenta)

├── 2. Registrar nuevo usuario# - SENDGRID_API_KEY1. **Clonar e instalar dependencias:**```

│   ├── Usuario (mín. 3 caracteres)

│   ├── Email válido# - MAILGUN_API_KEY y MAILGUN_DOMAIN

│   ├── Contraseña (mín. 6 caracteres)

│   ├── Confirmación de contraseña# - SUPABASE_URL y SUPABASE_KEY```bash

│   └── Validación anti-duplicados

└── Carga perfil del usuario```



📧 ENVÍO DE EMAILgit clone <repo>3. **Ejecutar:**

├── Solicita email destino

├── Solicita nombre destino## 🎯 Uso del Sistema

├── Solicita asunto

├── Solicita contenido HTMLcd Sirius-challenge```bash

├── Permite elegir proveedor

└── Usa EMAIL DEL USUARIO como remitente### Modo Interactivo (Principal)



🎛️ MENÚ PRINCIPAL```bashpython -m venv venvpython app_simple.py

├── 1. Enviar email

├── 2. Ver perfil# Ejecutar sistema interactivo

├── 3. Registrar otro usuario

└── 4. Salirpython app.pysource venv/bin/activate  # Linux/Mac```

```



## 🔒 Sistema de Registro Integrado

# Te pedirá:pip install -r requirements.txt

### Características del Registro:

- **Validación completa**: Usuario (3+ chars), email válido, contraseña (6+ chars)# 1. Usuario y contraseña

- **Anti-duplicados**: Verifica que usuario y email no existan

- **Contraseñas seguras**: Hashing con bcrypt# 2. Datos del destinatario```¡Listo! 🎉

- **Confirmación**: Doble verificación de contraseña

- **Inmediato**: Registro y login en una sesión# 3. Contenido del email



### Dónde registrarse:# 4. Proveedor preferido

1. **Al iniciar**: Selecciona "2. Registrar nuevo usuario"

2. **En menú principal**: Opción "3. Registrar otro usuario"```



## 🔒 Seguridad Integrada2. **Configurar variables de entorno:**## 📝 Uso Súper Fácil



- **Solo emails autorizados**: El sistema usa automáticamente el email del usuario logueado como remitente### Modo API (Opcional)

- **Autenticación obligatoria**: No se puede enviar emails sin login

- **Passwords hasheados**: Bcrypt para máxima seguridad```bash```bash

- **Validación completa**: Verificación de entrada en todos los campos

- **Base de datos segura**: Supabase con autenticación# Ejecutar como API REST



## 📋 API Endpoints (Modo --api)python app.py --apicp .env.example .env### 1. Registrar usuario



### Autenticación```

```bash

# Registrar usuario# Editar .env con tus credenciales:```bash

POST /registro

{## 📱 Flujo de Uso Interactivo

  "username": "usuario",

  "email": "email@ejemplo.com", # - SENDGRID_API_KEYcurl -X POST http://localhost:5000/registro \

  "password": "contraseña"

}```



# Iniciar sesión🔐 AUTENTICACIÓN# - MAILGUN_API_KEY y MAILGUN_DOMAIN  -H "Content-Type: application/json" \

POST /login

{├── Pide usuario/contraseña por terminal

  "username": "usuario",

  "password": "contraseña"├── Valida en base de datos Supabase# - SUPABASE_URL y SUPABASE_KEY  -d '{"username": "juan", "email": "juan@test.com", "password": "123456"}'

}

```└── Carga perfil del usuario



### Email (requiere JWT token)``````

```bash

# Envío automático (elige el mejor proveedor)📧 ENVÍO DE EMAIL

POST /enviar-email

Authorization: Bearer <token>├── Solicita email destino

{

  "to_email": "destinatario@ejemplo.com",├── Solicita nombre destino

  "to_name": "Nombre",

  "subject": "Asunto",├── Solicita asunto3. **Ejecutar:**### 2. Hacer login

  "html_content": "<h1>Contenido HTML</h1>"

}├── Solicita contenido HTML



# Envío con proveedor específico├── Permite elegir proveedor```bash```bash

POST /enviar-email

Authorization: Bearer <token>└── Usa EMAIL DEL USUARIO como remitente

{

  "to_email": "destinatario@ejemplo.com",python app.pycurl -X POST http://localhost:5000/login \

  "to_name": "Nombre", 

  "subject": "Asunto",🎛️ MENÚ PRINCIPAL

  "html_content": "<h1>Contenido HTML</h1>",

  "provider": "sendgrid",  // o "mailgun"├── 1. Enviar email```  -H "Content-Type: application/json" \

  "use_fallback": true     // fallback si falla

}├── 2. Ver perfil

```

└── 3. Salir  -d '{"username": "juan", "password": "123456"}'

## 🔧 Arquitectura

```

```

EmailService## 📋 API Endpoints```

├── SendGridProvider    (Proveedor 1)

├── MailgunProvider     (Proveedor 2)  ## 🔒 Seguridad Integrada

└── Fallback Logic      (Automático)



UserSystem

├── Registro Terminal   (Crear usuarios)- **Solo emails autorizados**: El sistema usa automáticamente el email del usuario logueado como remitente

├── Login Terminal      (Autenticación)

├── Supabase DB        (Almacenamiento)- **Autenticación obligatoria**: No se puede enviar emails sin login### Autenticación### 3. Enviar email (usar el token del login)

└── Bcrypt Security    (Contraseñas)

```- **Passwords hasheados**: Bcrypt para máxima seguridad



### Proveedores Disponibles:- **Validación completa**: Verificación de entrada en todos los campos```bash```bash

- **SendGrid**: Proveedor principal confiable

- **Mailgun**: Proveedor de respaldo robusto



### Lógica de Fallback:## 📋 API Endpoints (Modo --api)# Registrar usuariocurl -X POST http://localhost:5000/enviar-email \

1. Intenta con proveedor especificado (o primero disponible)

2. Si falla y `use_fallback=true`, prueba con el siguiente

3. Retorna resultado exitoso o error detallado

### AutenticaciónPOST /registro  -H "Content-Type: application/json" \

## 🧪 Pruebas

```bash

```bash

# Probar sistema de registro# Registrar usuario{  -H "Authorization: Bearer TU_TOKEN_AQUI" \

python test_registro.py

POST /registro

# Probar sistema interactivo completo

python test_interactive.py{  "username": "usuario",  -d '{



# Probar ambos proveedores directamente  "username": "usuario",

python test_providers.py

  "email": "email@ejemplo.com",   "email": "email@ejemplo.com",     "to_email": "destino@test.com",

# Probar API completa

curl -X POST http://localhost:5000/login \  "password": "contraseña"

  -H "Content-Type: application/json" \

  -d '{"username": "usuario", "password": "contraseña"}'}  "password": "contraseña"    "to_name": "Destinatario",

```



## 📁 Estructura del Proyecto

# Iniciar sesión}    "subject": "¡Hola!",

```

├── app.py              # Sistema principal (interactivo + API)POST /login

├── email_service.py    # Servicio multi-proveedor

├── test_providers.py   # Tests de proveedores  {    "html_content": "<p>Este es un email de prueba</p>"

├── test_interactive.py # Test del modo interactivo

├── test_registro.py    # Test del sistema de registro  "username": "usuario",

├── send_email.py       # Script de prueba simple

├── requirements.txt    # Dependencias  "password": "contraseña"# Iniciar sesión  }'

├── .env               # Variables de entorno

└── README.md          # Documentación}

```

```POST /login```

## 🎮 Ejemplo de Uso Completo



```bash

$ python app.py### Email (requiere JWT token){



🚀 INICIANDO MODO INTERACTIVO```bash

Conectando a servicios...

✅ Conectado a Supabase# Envío automático (elige el mejor proveedor)  "username": "usuario",## 🔑 Endpoints

📧 Proveedores de email configurados: sendgrid, mailgun

POST /enviar-email

==================================================

🔐 SISTEMA DE EMAIL - AUTENTICACIÓNAuthorization: Bearer <token>  "password": "contraseña"

==================================================

{

¿Qué deseas hacer?

1. 🔑 Iniciar sesión  "to_email": "destinatario@ejemplo.com",}- `POST /registro` - Crear usuario

2. 📝 Registrar nuevo usuario

  "to_name": "Nombre",

🔢 Selecciona una opción (1-2): 2

  "subject": "Asunto",```- `POST /login` - Iniciar sesión (devuelve token)

==================================================

📝 SISTEMA DE EMAIL - REGISTRO DE USUARIO  "html_content": "<h1>Contenido HTML</h1>"

==================================================

}- `GET /perfil` - Ver perfil (requiere token)

📋 Datos del nuevo usuario:

👤 Usuario (mín. 3 caracteres): nuevo_usuario

📧 Email: nuevo@empresa.com

🔒 Contraseña (mín. 6 caracteres): [oculta]# Envío con proveedor específico### Email (requiere JWT token)- `POST /enviar-email` - Enviar email (requiere token)

🔒 Confirmar contraseña: [oculta]

POST /enviar-email

🚀 Creando usuario...

Authorization: Bearer <token>```bash- `GET /health` - Verificar API

✅ ¡Usuario nuevo_usuario registrado exitosamente!

📧 Email: nuevo@empresa.com{

🔑 Ya puedes iniciar sesión

  "to_email": "destinatario@ejemplo.com",# Envío automático (elige el mejor proveedor)

🔄 Ahora puedes iniciar sesión...

  "to_name": "Nombre", 

🔑 Login - Intento 1 de 3

👤 Usuario: nuevo_usuario  "subject": "Asunto",POST /enviar-email## ⚙️ Configuración

🔒 Contraseña: [oculta]

  "html_content": "<h1>Contenido HTML</h1>",

✅ ¡Bienvenido/a nuevo_usuario!

📧 Email configurado: nuevo@empresa.com  "provider": "sendgrid",  // o "mailgun"Authorization: Bearer <token>



==================================================  "use_fallback": true     // fallback si falla

📧 SISTEMA DE EMAIL - MENÚ PRINCIPAL

==================================================}{Solo necesitas editar el archivo `.env`:

1. 📧 Enviar email

2. 👤 Ver perfil```

3. 📝 Registrar otro usuario

4. 👋 Salir  "to_email": "destinatario@ejemplo.com",



🔢 Selecciona una opción (1-4): 1## 🔧 Arquitectura



==================================================  "to_name": "Nombre",```env

📧 ENVIAR EMAIL

==================================================```



📋 Datos del destinatario:EmailService  "subject": "Asunto",SENDGRID_API_KEY=tu_clave_sendgrid

✉️  Email destino: cliente@empresa.com

👤 Nombre destino: Cliente VIP├── SendGridProvider    (Proveedor 1)



📝 Contenido del email:├── MailgunProvider     (Proveedor 2)    "html_content": "<h1>Contenido HTML</h1>"FROM_EMAIL=tu_email@ejemplo.com

📌 Asunto: Bienvenida al sistema

📄 Contenido HTML (presiona Enter dos veces para terminar):└── Fallback Logic      (Automático)

<h1>¡Hola Cliente VIP!</h1>

<p>Te damos la bienvenida a nuestro sistema.</p>```}JWT_SECRET=cualquier-texto-secreto

<p>Saludos cordiales.</p>





📡 Proveedores disponibles: sendgrid, mailgun### Proveedores Disponibles:```

🔧 Proveedor (presiona Enter para automático): 

- **SendGrid**: Proveedor principal confiable

🚀 Enviando email...

   De: nuevo@empresa.com- **Mailgun**: Proveedor de respaldo robusto# Envío con proveedor específico

   Para: cliente@empresa.com (Cliente VIP)

   Asunto: Bienvenida al sistema

   Proveedor: Automático

### Lógica de Fallback:POST /enviar-email## ✨ Características

✅ ¡Email enviado exitosamente!

📡 Proveedor usado: sendgrid1. Intenta con proveedor especificado (o primero disponible)

```

2. Si falla y `use_fallback=true`, prueba con el siguienteAuthorization: Bearer <token>

## 🚀 Producción

3. Retorna resultado exitoso o error detallado

Para producción, considera:

- Usar un servidor WSGI como Gunicorn{- ✅ Sin base de datos (usa archivo JSON)

- Configurar HTTPS/TLS

- Implementar rate limiting  ## 🧪 Pruebas

- Monitoreo de logs y métricas

- Backup de base de datos  "to_email": "destinatario@ejemplo.com",- ✅ Todo en un solo archivo



---```bash



**¡Sistema completo con registro listo para Challenge! 🏆**# Probar sistema interactivo  "to_name": "Nombre", - ✅ JWT que expira en 1 hora

python test_interactive.py

  "subject": "Asunto",- ✅ Contraseñas encriptadas

# Probar ambos proveedores directamente

python test_providers.py  "html_content": "<h1>Contenido HTML</h1>",- ✅ Súper simple de usar



# Probar API completa  "provider": "sendgrid",  // o "mailgun"

curl -X POST http://localhost:5000/login \

  -H "Content-Type: application/json" \  "use_fallback": true     // fallback si falla## 📁 Archivos que se crean

  -d '{"username": "usuario", "password": "contraseña"}'

```}



## 📁 Estructura del Proyecto```- `usuarios.json` - Base de datos local de usuarios



```- `.env` - Configuración

├── app.py              # Sistema principal (interactivo + API)

├── email_service.py    # Servicio multi-proveedor## 🔧 Arquitectura

├── test_providers.py   # Tests de proveedores  

├── test_interactive.py # Test del modo interactivo¡Eso es todo! 🎯

├── send_email.py       # Script de prueba simple```

├── requirements.txt    # DependenciasEmailService

├── .env               # Variables de entorno├── SendGridProvider    (Proveedor 1)

└── README.md          # Documentación├── MailgunProvider     (Proveedor 2)  

```└── Fallback Logic      (Automático)

```

## 🎮 Ejemplo de Uso Interactivo

### Proveedores Disponibles:

```bash- **SendGrid**: Proveedor principal confiable

$ python app.py- **Mailgun**: Proveedor de respaldo robusto



🚀 INICIANDO MODO INTERACTIVO### Lógica de Fallback:

Conectando a servicios...1. Intenta con proveedor especificado (o primero disponible)

✅ Conectado a Supabase2. Si falla y `use_fallback=true`, prueba con el siguiente

📧 Proveedores de email configurados: sendgrid, mailgun3. Retorna resultado exitoso o error detallado



==================================================## 🧪 Pruebas

🔐 SISTEMA DE EMAIL - AUTENTICACIÓN

==================================================```bash

# Probar ambos proveedores

Intento 1 de 3python test_providers.py

👤 Usuario: martin

🔒 Contraseña: [oculta]# Probar API completa

curl -X POST http://localhost:5000/login \

✅ ¡Bienvenido/a martin!  -H "Content-Type: application/json" \

📧 Email configurado: martin@ejemplo.com  -d '{"username": "usuario", "password": "contraseña"}'

```

==================================================

📧 SISTEMA DE EMAIL - MENÚ PRINCIPAL## 📁 Estructura del Proyecto

==================================================

1. 📧 Enviar email```

2. 👤 Ver perfil├── app.py              # API principal Flask

3. 👋 Salir├── email_service.py    # Servicio multi-proveedor

├── test_providers.py   # Tests de proveedores  

🔢 Selecciona una opción (1-3): 1├── send_email.py       # Script de prueba simple

├── requirements.txt    # Dependencias

==================================================├── .env               # Variables de entorno

📧 ENVIAR EMAIL└── README.md          # Documentación

==================================================```



📋 Datos del destinatario:## 🔒 Seguridad

✉️  Email destino: cliente@empresa.com

👤 Nombre destino: Cliente Importante- Passwords hasheados con bcrypt

- JWT tokens con expiración configurable  

📝 Contenido del email:- Validación de entrada en todos los endpoints

📌 Asunto: Propuesta comercial- Manejo seguro de credenciales via variables de entorno

📄 Contenido HTML (presiona Enter dos veces para terminar):

<h1>Hola Cliente!</h1>## 🚀 Producción

<p>Te envío la propuesta que discutimos.</p>

<p>Saludos!</p>Para producción, considera:

- Usar un servidor WSGI como Gunicorn

- Configurar HTTPS/TLS

📡 Proveedores disponibles: sendgrid, mailgun- Implementar rate limiting  

🔧 Proveedor (presiona Enter para automático): - Monitoreo de logs y métricas

- Backup de base de datos

🚀 Enviando email...

   De: martin@ejemplo.com---

   Para: cliente@empresa.com (Cliente Importante)

   Asunto: Propuesta comercial**¡Sistema listo para Challenge! 🏆**
   Proveedor: Automático

✅ ¡Email enviado exitosamente!
📡 Proveedor usado: sendgrid
```

## 🚀 Producción

Para producción, considera:
- Usar un servidor WSGI como Gunicorn
- Configurar HTTPS/TLS
- Implementar rate limiting  
- Monitoreo de logs y métricas
- Backup de base de datos

---

**¡Sistema interactivo listo para Challenge! 🏆**