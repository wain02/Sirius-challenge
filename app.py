#!/usr/bin/env python3
"""
Sistema de Email Interactivo por Terminal
- Autenticación por terminal
- Envío de emails interactivo
- Solo el email del usuario logueado puede enviar
"""

import os
import json
import jwt
import bcrypt
import requests
import getpass
import sys
from datetime import datetime, timedelta
from flask import Flask, request, jsonify
from flask_cors import CORS
from functools import wraps
from dotenv import load_dotenv
from supabase import create_client, Client
from email_service import EmailService

# Cargar variables de entorno
load_dotenv()

# Crear app Flask
app = Flask(__name__)
CORS(app)

# Configuración
JWT_SECRET = os.getenv('JWT_SECRET', 'mi-clave-secreta-super-segura')
SENDGRID_API_KEY = os.getenv('SENDGRID_API_KEY')
FROM_EMAIL = os.getenv('FROM_EMAIL', 'mwainwright@fi.uba.ar')

# Configuración de Mailgun
MAILGUN_API_KEY = os.getenv('MAILGUN_API_KEY')
MAILGUN_DOMAIN = os.getenv('MAILGUN_DOMAIN')
MAILGUN_FROM_EMAIL = os.getenv('MAILGUN_FROM_EMAIL')

# Configuración de Supabase
SUPABASE_URL = os.getenv('SUPABASE_URL')
SUPABASE_KEY = os.getenv('SUPABASE_KEY')

if not SUPABASE_URL or not SUPABASE_KEY:
    raise ValueError("❌ SUPABASE_URL y SUPABASE_KEY son requeridas en el archivo .env")

# Crear cliente de Supabase
supabase: Client = create_client(SUPABASE_URL, SUPABASE_KEY)
print("✅ Conectado a Supabase")

# Configurar servicio de email
email_service = EmailService(
    sendgrid_api_key=SENDGRID_API_KEY,
    mailgun_api_key=MAILGUN_API_KEY,
    mailgun_domain=MAILGUN_DOMAIN
)

# Mostrar proveedores configurados
proveedores = email_service.get_available_providers()
print(f"📧 Proveedores de email configurados: {', '.join(proveedores)}")

# Funciones de base de datos
def buscar_usuario(username):
    """Buscar usuario por username en Supabase"""
    try:
        result = supabase.table('users').select('*').eq('username', username).execute()
        if result.data:
            user = result.data[0]
            return {
                'id': user['id'],
                'username': username,
                'email': user['email'],
                'password': user['password_hash'],
                'fecha_registro': user['created_at']
            }
        return None
    except Exception as e:
        print(f"❌ Error buscando usuario: {e}")
        return None

def crear_usuario(username, email, password_hash):
    """Crear usuario en Supabase"""
    try:
        result = supabase.table('users').insert({
            'username': username,
            'email': email,
            'password_hash': password_hash
        }).execute()
        
        if result.data:
            return True, result.data[0]
        return False, "Error al crear usuario"
    except Exception as e:
        print(f"❌ Error creando usuario: {e}")
        return False, str(e)

def verificar_usuario_existe(username, email):
    """Verificar si username o email ya existen"""
    try:
        # Verificar username
        result_username = supabase.table('users').select('id').eq('username', username).execute()
        if result_username.data:
            return True, "El nombre de usuario ya existe"
        
        # Verificar email
        result_email = supabase.table('users').select('id').eq('email', email).execute()
        if result_email.data:
            return True, "El email ya existe"
        
        return False, None
    except Exception as e:
        print(f"❌ Error verificando usuario: {e}")
        return True, str(e)

def registrar_email_enviado(user_id, username, from_email, to_email, to_name, subject, html_content, provider_usado, estado):
    """Registrar email enviado en la tabla email_logs"""
    try:
        log_data = {
            'user_id': user_id,
            'username': username,
            'from_email': from_email,
            'to_email': to_email,
            'subject': subject,
            'html_content': html_content,
            'provider_usado': provider_usado,
            'estado': estado,  # 'exitoso' o 'fallido'
            'created_at': datetime.utcnow().isoformat()
        }
        
        result = supabase.table('email_logs').insert(log_data).execute()
        
        if result.data:
            return True
        return False
        
    except Exception as e:
        print(f"❌ Error registrando email log: {e}")
        return False

def obtener_historial_emails(user_id, limite=10):
    """Obtener historial de emails enviados por el usuario"""
    try:
        result = supabase.table('email_logs').select('*').eq('user_id', user_id).order('created_at', desc=True).limit(limite).execute()
        
        if result.data:
            return result.data
        return []
        
    except Exception as e:
        print(f"❌ Error obteniendo historial: {e}")
        return []

def encriptar_password(password):
    """Encriptar contraseña"""
    return bcrypt.hashpw(password.encode('utf-8'), bcrypt.gensalt()).decode('utf-8')

def verificar_password(password, hash_password):
    """Verificar contraseña"""
    return bcrypt.checkpw(password.encode('utf-8'), hash_password.encode('utf-8'))

def generar_token(username):
    """Generar token JWT"""
    payload = {
        'username': username,
        'exp': datetime.utcnow() + timedelta(hours=1),  # ⏰ CAMBIAR AQUÍ: hours=1 (1 hora)
        'iat': datetime.utcnow()  # 📅 Fecha cuando se creó el token
    }
    return jwt.encode(payload, JWT_SECRET, algorithm='HS256')

def verificar_token(token):
    """Verificar token JWT"""
    try:
        payload = jwt.decode(token, JWT_SECRET, algorithms=['HS256'])
        return True, payload['username']
    except jwt.ExpiredSignatureError:
        return False, "Token expirado"
    except jwt.InvalidTokenError:
        return False, "Token inválido"

# Decorador para rutas protegidas
def login_requerido(f):
    @wraps(f)
    def decorated(*args, **kwargs):
        token = request.headers.get('Authorization')
        
        if not token:
            return jsonify({'error': 'Token requerido'}), 401
        
        if token.startswith('Bearer '):
            token = token[7:]
        
        valido, resultado = verificar_token(token)
        if not valido:
            return jsonify({'error': resultado}), 401
        
        request.usuario_actual = resultado
        return f(*args, **kwargs)
    
    return decorated

# RUTAS

@app.route('/health')
def salud():
    """Verificar que la API funciona"""
    return jsonify({'estado': 'ok', 'mensaje': 'API funcionando correctamente'})

@app.route('/registro', methods=['POST'])
def registro():
    """Registrar nuevo usuario"""
    try:
        datos = request.get_json()
        
        if not datos or not all(k in datos for k in ('username', 'email', 'password')):
            return jsonify({'error': 'username, email y password son requeridos'}), 400
        
        username = datos['username'].strip()
        email = datos['email'].strip()
        password = datos['password']
        
        if len(username) < 3:
            return jsonify({'error': 'Username debe tener al menos 3 caracteres'}), 400
        
        if len(password) < 6:
            return jsonify({'error': 'Password debe tener al menos 6 caracteres'}), 400
        
        # Verificar si usuario ya existe
        existe, mensaje = verificar_usuario_existe(username, email)
        if existe:
            return jsonify({'error': mensaje}), 400
        
        # Crear usuario
        password_hash = encriptar_password(password)
        exito, resultado = crear_usuario(username, email, password_hash)
        
        if exito:
            return jsonify({
                'mensaje': 'Usuario registrado exitosamente',
                'usuario': {'username': username, 'email': email}
            }), 201
        else:
            return jsonify({'error': f'Error al registrar: {resultado}'}), 500
        
    except Exception as e:
        return jsonify({'error': f'Error en el registro: {str(e)}'}), 500

@app.route('/login', methods=['POST'])
def login():
    """Iniciar sesión"""
    try:
        datos = request.get_json()
        
        if not datos or not all(k in datos for k in ('username', 'password')):
            return jsonify({'error': 'username y password son requeridos'}), 400
        
        username = datos['username'].strip()
        password = datos['password']
        
        usuario = buscar_usuario(username)
        
        if not usuario:
            return jsonify({'error': 'Usuario o contraseña incorrectos'}), 401
        
        if not verificar_password(password, usuario['password']):
            return jsonify({'error': 'Usuario o contraseña incorrectos'}), 401
        
        token = generar_token(username)
        
        return jsonify({
            'mensaje': 'Login exitoso',
            'token': token,
            'expira_en': '1 hora'
        })
        
    except Exception as e:
        return jsonify({'error': f'Error en el login: {str(e)}'}), 500

@app.route('/perfil')
@login_requerido
def perfil():
    """Obtener perfil del usuario"""
    try:
        usuario = buscar_usuario(request.usuario_actual)
        
        if not usuario:
            return jsonify({'error': 'Usuario no encontrado'}), 404
        
        return jsonify({
            'usuario': {
                'username': request.usuario_actual,
                'email': usuario['email'],
                'fecha_registro': usuario['fecha_registro']
            }
        })
        
    except Exception as e:
        return jsonify({'error': f'Error al obtener perfil: {str(e)}'}), 500

@app.route('/enviar-email', methods=['POST'])
@login_requerido
def enviar_email():
    """Enviar email con soporte para múltiples proveedores (requiere autenticación)"""
    try:
        datos = request.get_json()
        
        campos_requeridos = ['to_email', 'to_name', 'subject', 'html_content']
        if not datos or not all(k in datos for k in campos_requeridos):
            return jsonify({'error': f'Campos requeridos: {", ".join(campos_requeridos)}'}), 400
        
        # Obtener parámetros opcionales
        proveedor = datos.get('provider')  # 'sendgrid', 'mailgun' o None para auto
        usar_fallback = datos.get('use_fallback', True)
        
        # Determinar el email de origen según el proveedor
        if proveedor == 'mailgun' and MAILGUN_FROM_EMAIL:
            from_email = MAILGUN_FROM_EMAIL
        else:
            from_email = FROM_EMAIL
        
        # Enviar email usando el servicio
        resultado = email_service.send_email(
            from_email=from_email,
            to_email=datos['to_email'],
            to_name=datos['to_name'],
            subject=datos['subject'],
            html_content=datos['html_content'],
            substitutions=datos.get('substitutions'),
            provider=proveedor,
            use_fallback=usar_fallback
        )
        
        if resultado.get('success'):
            return jsonify({
                'mensaje': 'Email enviado exitosamente',
                'proveedor_usado': resultado.get('provider'),
                'enviado_por': request.usuario_actual,
                'proveedores_disponibles': email_service.get_available_providers()
            })
        else:
            return jsonify({
                'error': 'Error al enviar email',
                'proveedor_intentado': resultado.get('provider'),
                'detalles': resultado.get('error', resultado.get('response_text')),
                'codigo_estado': resultado.get('status_code')
            }), 500
            
    except Exception as e:
        return jsonify({'error': f'Error al enviar email: {str(e)}'}), 500

# Manejadores de error
@app.errorhandler(404)
def no_encontrado(error):
    return jsonify({'error': 'Endpoint no encontrado'}), 404

@app.errorhandler(405)
def metodo_no_permitido(error):
    return jsonify({'error': 'Método no permitido'}), 405

# ==========================================
# SISTEMA INTERACTIVO POR TERMINAL
# ==========================================

def registro_terminal():
    """Registro de nuevo usuario por terminal"""
    print("\n" + "="*50)
    print("📝 SISTEMA DE EMAIL - REGISTRO DE USUARIO")
    print("="*50)
    
    try:
        # Solicitar datos del usuario
        print("\n📋 Datos del nuevo usuario:")
        
        while True:
            username = input("👤 Usuario (mín. 3 caracteres): ").strip()
            if len(username) >= 3:
                break
            print("❌ El usuario debe tener al menos 3 caracteres")
        
        while True:
            email = input("📧 Email: ").strip()
            if "@" in email and "." in email:
                break
            print("❌ Email inválido")
        
        while True:
            password = getpass.getpass("🔒 Contraseña (mín. 6 caracteres): ")
            if len(password) >= 6:
                break
            print("❌ La contraseña debe tener al menos 6 caracteres")
        
        password_confirm = getpass.getpass("🔒 Confirmar contraseña: ")
        
        if password != password_confirm:
            print("❌ Las contraseñas no coinciden")
            return False
        
        # Verificar si usuario ya existe
        existe, mensaje = verificar_usuario_existe(username, email)
        if existe:
            print(f"❌ {mensaje}")
            return False
        
        # Crear usuario
        print("\n🚀 Creando usuario...")
        password_hash = encriptar_password(password)
        exito, resultado = crear_usuario(username, email, password_hash)
        
        if exito:
            print(f"\n✅ ¡Usuario {username} registrado exitosamente!")
            print(f"📧 Email: {email}")
            print("🔑 Ya puedes iniciar sesión")
            return True
        else:
            print(f"❌ Error al registrar: {resultado}")
            return False
            
    except KeyboardInterrupt:
        print("\n\n👋 Registro cancelado")
        return False
    except Exception as e:
        print(f"❌ Error en el registro: {e}")
        return False

def menu_inicial():
    """Menú inicial: Login o Registro"""
    while True:
        try:
            print("\n" + "="*50)
            print("🚀 SISTEMA DE EMAIL - BIENVENIDO")
            print("="*50)
            print("1. 🔐 Iniciar sesión")
            print("2. 📝 Registrar nuevo usuario")
            print("3. 🚪 Salir")
            
            opcion = input("\n🔢 Selecciona una opción (1-3): ").strip()
            
            if opcion == "1":
                usuario = login_terminal()
                if usuario:
                    return usuario
            elif opcion == "2":
                registro_terminal()
                print("\n✅ Usuario registrado. Ahora puedes iniciar sesión.")
            elif opcion == "3":
                print("\n👋 ¡Hasta luego!")
                sys.exit(0)
            else:
                print("❌ Opción inválida. Usa 1, 2 o 3.")
                
        except KeyboardInterrupt:
            print("\n\n👋 ¡Hasta luego!")
            sys.exit(0)
        except Exception as e:
            print(f"❌ Error: {e}")

def login_terminal():
    """Autenticación por terminal"""
    print("\n" + "="*50)
    print("🔐 INICIO DE SESIÓN")
    print("="*50)
    
    # Proceso de login directo
    max_intentos = 3
    for intento in range(max_intentos):
        try:
            print(f"\n🔑 Intento {intento + 1} de {max_intentos}")
            username = input("👤 Usuario: ").strip()
            
            if not username:
                print("❌ El usuario no puede estar vacío")
                continue
            
            password = getpass.getpass("🔒 Contraseña: ")
            
            if not password:
                print("❌ La contraseña no puede estar vacía")
                continue
            
            # Verificar credenciales
            usuario = buscar_usuario(username)
            
            if not usuario:
                print("❌ Usuario o contraseña incorrectos")
                continue
            
            if not verificar_password(password, usuario['password']):
                print("❌ Usuario o contraseña incorrectos")
                continue
            
            # Login exitoso
            print(f"\n✅ ¡Bienvenido/a {username}!")
            print(f"📧 Email configurado: {usuario['email']}")
            return usuario
            
        except KeyboardInterrupt:
            print("\n\n👋 Proceso cancelado por el usuario")
            sys.exit(0)
        except Exception as e:
            print(f"❌ Error: {e}")
    
    print(f"\n❌ Máximo de intentos alcanzado ({max_intentos})")
    return None

def enviar_email_interactivo(usuario_actual):
    """Envío de email interactivo por terminal"""
    try:
        print("\n" + "="*50)
        print("📧 ENVIAR EMAIL")
        print("="*50)
        
        # Datos del destinatario
        print("\n📋 Datos del destinatario:")
        to_email = input("✉️  Email destino: ").strip()
        if not to_email:
            print("❌ Email destino es requerido")
            return
        
        to_name = input("👤 Nombre destino: ").strip()
        if not to_name:
            to_name = to_email
        
        # Contenido del email
        print("\n📝 Contenido del email:")
        subject = input("📌 Asunto: ").strip()
        if not subject:
            print("❌ Asunto es requerido")
            return
        
        print("📄 Contenido HTML (presiona Enter dos veces para terminar):")
        html_lines = []
        while True:
            line = input()
            if line == "" and html_lines and html_lines[-1] == "":
                break
            html_lines.append(line)
        
        html_content = "\n".join(html_lines).strip()
        if not html_content:
            html_content = f"<p>{subject}</p>"
        
        # Selección de proveedor
        print(f"\n📡 Proveedores disponibles: {', '.join(email_service.get_available_providers())}")
        proveedor = input("🔧 Proveedor (presiona Enter para automático): ").strip().lower()
        if proveedor and proveedor not in email_service.get_available_providers():
            proveedor = None
        
        # Usar el email del usuario como remitente
        from_email = usuario_actual['email']
        
        print(f"\n🚀 Enviando email...")
        print(f"   De: {from_email}")
        print(f"   Para: {to_email} ({to_name})")
        print(f"   Asunto: {subject}")
        print(f"   Proveedor: {'Automático' if not proveedor else proveedor}")
        
        # Enviar email
        resultado = email_service.send_email(
            from_email=from_email,
            to_email=to_email,
            to_name=to_name,
            subject=subject,
            html_content=html_content,
            provider=proveedor if proveedor else None,
            use_fallback=True
        )
        
        # Registrar el envío en la base de datos
        estado = 'exitoso' if resultado.get('success') else 'fallido'
        provider_usado = resultado.get('provider', 'desconocido')
        
        log_registrado = registrar_email_enviado(
            user_id=usuario_actual['id'],
            username=usuario_actual['username'],
            from_email=from_email,
            to_email=to_email,
            to_name=to_name,
            subject=subject,
            html_content=html_content,
            provider_usado=provider_usado,
            estado=estado
        )
        
        if resultado.get('success'):
            print(f"\n✅ ¡Email enviado exitosamente!")
            print(f"📡 Proveedor usado: {resultado.get('provider')}")
            if log_registrado:
                print("📝 Envío registrado en el historial")
            else:
                print("⚠️  Email enviado pero no se pudo registrar en la base de datos")
        else:
            print(f"\n❌ Error al enviar email:")
            print(f"   Proveedor: {resultado.get('provider')}")
            print(f"   Error: {resultado.get('error', resultado.get('response_text'))}")
            if log_registrado:
                print("📝 Error registrado en el historial")
            else:
                print("⚠️  No se pudo registrar el error en la base de datos")
            
    except KeyboardInterrupt:
        print("\n\n📧 Envío cancelado")
    except Exception as e:
        print(f"\n❌ Error: {e}")

def mostrar_perfil(usuario_actual):
    """Mostrar perfil del usuario"""
    print("\n" + "="*50)
    print("👤 PERFIL DE USUARIO")
    print("="*50)
    
    # Buscar datos actualizados del usuario
    usuario_db = buscar_usuario(usuario_actual.get('username', ''))
    if usuario_db:
        print(f"👤 Usuario: {usuario_db.get('username', usuario_actual.get('username', 'N/A'))}")
        print(f"📧 Email: {usuario_db['email']}")
        print(f"📅 Registrado: {usuario_db.get('fecha_registro', 'N/A')}")
    else:
        print(f"👤 Usuario: {usuario_actual.get('username', 'N/A')}")
        print(f"📧 Email: {usuario_actual['email']}")
        print(f"📅 Registrado: {usuario_actual.get('fecha_registro', 'N/A')}")
    
    print(f"🔧 Proveedores: {', '.join(email_service.get_available_providers())}")

def mostrar_historial_emails(usuario_actual):
    """Mostrar historial de emails enviados"""
    print("\n" + "="*50)
    print("📜 HISTORIAL DE EMAILS ENVIADOS")
    print("="*50)
    
    try:
        # Obtener historial del usuario
        historial = obtener_historial_emails(usuario_actual['id'], limite=20)
        
        if not historial:
            print("\n📭 No hay emails en el historial")
            return
        
        print(f"\n📊 Últimos {len(historial)} emails enviados:")
        print("-" * 80)
        
        for i, email in enumerate(historial, 1):
            # Formatear fecha
            try:
                fecha_str = email['created_at']
                if 'T' in fecha_str:
                    fecha_formateada = fecha_str.split('T')[0] + ' ' + fecha_str.split('T')[1][:8]
                else:
                    fecha_formateada = fecha_str
            except:
                fecha_formateada = email.get('created_at', 'N/A')
            
            # Estado con emoji
            estado_emoji = "✅" if email['estado'] == 'exitoso' else "❌"
            
            print(f"\n{i}. {estado_emoji} {email['estado'].upper()}")
            print(f"   📅 Fecha: {fecha_formateada}")
            print(f"   📧 Para: {email['to_email']}")
            print(f"   📌 Asunto: {email['subject']}")
            print(f"   🔧 Proveedor: {email['provider_usado']}")
            
            # Mostrar contenido (truncado)
            content = email.get('html_content', '')
            if len(content) > 100:
                content = content[:100] + "..."
            print(f"   📄 Contenido: {content}")
            
        print("\n" + "="*50)
        
    except Exception as e:
        print(f"❌ Error al obtener historial: {e}")

def menu_principal(usuario_actual):
    """Menú principal interactivo"""
    while True:
        try:
            print("\n" + "="*50)
            print("📧 SISTEMA DE EMAIL - MENÚ PRINCIPAL")
            print("="*50)
            print("1. 📧 Enviar email")
            print("2. 👤 Ver perfil")
            print("3. � Ver historial de emails")
            print("4. �👋 Salir")
            
            opcion = input("\n🔢 Selecciona una opción (1-4): ").strip()
            
            if opcion == "1":
                enviar_email_interactivo(usuario_actual)
            elif opcion == "2":
                mostrar_perfil(usuario_actual)
            elif opcion == "3":
                mostrar_historial_emails(usuario_actual)
            elif opcion == "4":
                print("\n👋 ¡Hasta luego!")
                sys.exit(0)
            else:
                print("❌ Opción inválida. Usa 1, 2, 3 o 4.")
                
        except KeyboardInterrupt:
            print("\n\n👋 ¡Hasta luego!")
            sys.exit(0)
        except Exception as e:
            print(f"❌ Error: {e}")

def modo_interactivo():
    """Modo interactivo principal"""
    print("🚀 INICIANDO MODO INTERACTIVO")
    print("Conectando a servicios...")
    
    # Menú inicial (Login o Registro)
    usuario_actual = menu_inicial()
    
    # Menú principal
    menu_principal(usuario_actual)

if __name__ == '__main__':
    import sys
    
    if len(sys.argv) > 1 and sys.argv[1] == '--api':
        # Modo API
        print("Iniciando API de Email")
        print("Endpoints disponibles:")
        print("   POST /registro - Registrar usuario")
        print("   POST /login - Iniciar sesión")
        print("   GET  /perfil - Ver perfil (requiere token)")
        print("   POST /enviar-email - Enviar email (requiere token)")
        print("   GET  /health - Verificar API")
        print(f"🌐 Servidor corriendo en: http://localhost:5000")
        
        app.run(debug=True, port=5000)
    else:
        # Modo interactivo (por defecto)
        modo_interactivo()