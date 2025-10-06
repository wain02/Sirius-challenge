#!/usr/bin/env python3
"""
Script simple para enviar emails usando SendGrid
Basado en el ejemplo de request proporcionado
"""

import os
import sys
from dotenv import load_dotenv
from email_service import EmailService

# Cargar variables de entorno
load_dotenv()

def main():
    # Obtener clave API de SendGrid desde variables de entorno
    API_KEY = os.getenv('SENDGRID_API_KEY')
    
    if not API_KEY:
        print("❌ Error: SENDGRID_API_KEY no encontrada en las variables de entorno")
        print("Por favor revisa tu archivo .env o configura la variable de entorno")
        return
    
    # Inicializar servicio de email
    email_service = EmailService(API_KEY)
    
    # Configuración del email (desde variables de entorno o valores por defecto)
    from_email = os.getenv('FROM_EMAIL', "mwainwright@fi.uba.ar")
    to_email = os.getenv('TO_EMAIL', "martinwain2002@gmail.com")
    to_name = "Destinatario"
    subject = "hey there *names*"
    
    # Contenido HTML con variables de plantilla
    html_content = "<p>Dear *names*,</p><p>Your score was *scores*</p><p>Thanks!</p>"
    
    # Sustituciones para variables de plantilla
    substitutions = {
        "*names*": "tere",
        "*scores*": "98"
    }
    
    # Enviar email
    print("📧 Enviando email...")
    result = email_service.send_email(
        from_email=from_email,
        to_email=to_email,
        to_name=to_name,
        subject=subject,
        html_content=html_content,
        substitutions=substitutions
    )
    
    # Mostrar resultado
    if result["success"]:
        print("✅ ¡Email enviado exitosamente!")
        print(f"Código de estado: {result['status_code']}")
    else:
        print("❌ Error al enviar email")
        print(f"Código de estado: {result['status_code']}")
        print(f"Respuesta: {result['response_text']}")
        if "error" in result:
            print(f"Error: {result['error']}")


if __name__ == "__main__":
    main()