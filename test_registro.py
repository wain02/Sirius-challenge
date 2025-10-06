#!/usr/bin/env python3
"""
Script de prueba para el sistema de registro
"""

import os
from dotenv import load_dotenv

def main():
    print("🧪 PRUEBA DEL SISTEMA DE REGISTRO")
    print("="*50)
    
    # Cargar variables de entorno
    load_dotenv()
    
    # Verificar variables de entorno necesarias
    required_vars = ['SUPABASE_URL', 'SUPABASE_KEY']
    missing_vars = []
    
    for var in required_vars:
        if not os.getenv(var):
            missing_vars.append(var)
    
    if missing_vars:
        print(f"❌ Variables faltantes en .env: {', '.join(missing_vars)}")
        print("   Configura estas variables para usar el registro")
        return
    
    print("✅ Variables de Supabase configuradas")
    print("\n📋 INSTRUCCIONES:")
    print("1. Ejecuta: python app.py")
    print("2. En el menú inicial, selecciona '2' para registrar usuario")
    print("3. O en el menú principal, selecciona '3' para registrar otro usuario")
    print()
    print("📝 El sistema te pedirá:")
    print("   • Usuario (mínimo 3 caracteres)")
    print("   • Email válido")
    print("   • Contraseña (mínimo 6 caracteres)")
    print("   • Confirmación de contraseña")
    print()
    print("🔒 Funciones de seguridad:")
    print("   • Verificación de usuario/email duplicado")
    print("   • Contraseñas hasheadas con bcrypt")
    print("   • Validación de formato de email")
    print("   • Confirmación de contraseña")
    print()
    print("✅ Una vez registrado, podrás iniciar sesión inmediatamente")

if __name__ == "__main__":
    main()