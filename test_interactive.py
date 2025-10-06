#!/usr/bin/env python3
"""
Script de prueba rápida para el sistema interactivo
"""

import os
import subprocess
import sys

def main():
    print("🧪 PRUEBA RÁPIDA DEL SISTEMA INTERACTIVO")
    print("="*50)
    
    # Verificar que el archivo app.py existe
    if not os.path.exists("app.py"):
        print("❌ app.py no encontrado")
        return
    
    print("✅ app.py encontrado")
    
    # Verificar variables de entorno
    required_vars = ['SENDGRID_API_KEY', 'SUPABASE_URL', 'SUPABASE_KEY']
    missing_vars = []
    
    for var in required_vars:
        if not os.getenv(var):
            missing_vars.append(var)
    
    if missing_vars:
        print(f"⚠️  Variables faltantes en .env: {', '.join(missing_vars)}")
    else:
        print("✅ Variables de entorno configuradas")
    
    print("\n📋 INSTRUCCIONES DE USO:")
    print("1. Modo interactivo (por defecto):")
    print("   python app.py")
    print()
    print("2. Modo API:")
    print("   python app.py --api")
    print()
    print("🎯 El modo interactivo te pedirá usuario/contraseña")
    print("📧 Solo podrás enviar emails desde tu email registrado")
    print("🔧 Podrás elegir destinatario y proveedor")

if __name__ == "__main__":
    main()