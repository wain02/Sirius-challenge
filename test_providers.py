#!/usr/bin/env python3
"""
Script para probar los proveedores de email (SendGrid y Mailgun)
"""

import os
from dotenv import load_dotenv
from email_service import EmailService

# Cargar variables de entorno
load_dotenv()

def main():
    print("🧪 Test de proveedores de email")
    print("=" * 40)
    
    # Configurar servicio de email
    sendgrid_api_key = os.getenv('SENDGRID_API_KEY')
    mailgun_api_key = os.getenv('MAILGUN_API_KEY')
    mailgun_domain = os.getenv('MAILGUN_DOMAIN')
    
    if not sendgrid_api_key and not (mailgun_api_key and mailgun_domain):
        print("❌ Error: No hay proveedores configurados")
        return
    
    # Inicializar servicio
    email_service = EmailService(
        sendgrid_api_key=sendgrid_api_key,
        mailgun_api_key=mailgun_api_key,
        mailgun_domain=mailgun_domain
    )
    
    proveedores = email_service.get_available_providers()
    print(f"📧 Proveedores: {', '.join(proveedores)}")
    
    # Configuración del email
    from_email_sg = os.getenv('FROM_EMAIL', "mwainwright@fi.uba.ar")
    from_email_mg = os.getenv('MAILGUN_FROM_EMAIL')
    to_email = os.getenv('TO_EMAIL', "martinwain2002@gmail.com")
    
    # Test SendGrid
    if 'sendgrid' in proveedores:
        print("\n🔄 Probando SendGrid...")
        result = email_service.send_email(
            from_email=from_email_sg,
            to_email=to_email,
            to_name="Martin",
            subject="Test SendGrid - Sistema Multi-Proveedor 🚀",
            html_content="<h2>¡Hola!</h2><p>Email enviado con <strong>SendGrid</strong></p>",
            provider="sendgrid",
            use_fallback=False
        )
        status = "✅ Funciona" if result.get('success') else "❌ Error"
        print(f"   {status}")
    
    # Test Mailgun
    if 'mailgun' in proveedores:
        print("\n🔄 Probando Mailgun...")
        result = email_service.send_email(
            from_email=from_email_mg,
            to_email=to_email,
            to_name="Martin",
            subject="Test Mailgun - Sistema Multi-Proveedor 📬",
            html_content="<h2>¡Saludos!</h2><p>Email enviado con <strong>Mailgun</strong></p>",
            provider="mailgun",
            use_fallback=False
        )
        status = "✅ Funciona" if result.get('success') else "❌ Error"
        print(f"   {status}")
    
    # Test sistema automático
    if len(proveedores) > 1:
        print("\n🔄 Probando sistema automático...")
        result = email_service.send_email(
            from_email=from_email_sg if 'sendgrid' in proveedores else from_email_mg,
            to_email=to_email,
            to_name="Martin",
            subject="Test Sistema Automático 🤖",
            html_content="<h2>Sistema Multi-Proveedor</h2><p>Email con fallback automático</p>",
            use_fallback=True
        )
        status = "✅ Funciona" if result.get('success') else "❌ Error"
        provider = result.get('provider', 'unknown')
        print(f"   {status} (usó {provider})")
    
    print(f"\n🏁 Pruebas completadas - {len(proveedores)} proveedor(es)")

if __name__ == "__main__":
    main()