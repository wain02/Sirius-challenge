#!/usr/bin/env python3
"""
Script de prueba para el sistema de logging de emails
"""

import os
from dotenv import load_dotenv
from supabase import create_client

def test_email_logs():
    load_dotenv()
    
    # Configuración de Supabase
    SUPABASE_URL = os.getenv('SUPABASE_URL')
    SUPABASE_KEY = os.getenv('SUPABASE_KEY')
    
    if not SUPABASE_URL or not SUPABASE_KEY:
        print("❌ Variables de Supabase no configuradas")
        return
    
    try:
        # Conectar a Supabase
        supabase = create_client(SUPABASE_URL, SUPABASE_KEY)
        print("✅ Conectado a Supabase")
        
        # Verificar que la tabla email_logs existe
        result = supabase.table('email_logs').select('*').limit(1).execute()
        print("✅ Tabla email_logs encontrada")
        
        # Verificar que la tabla users existe
        result = supabase.table('users').select('*').limit(1).execute()
        print("✅ Tabla users encontrada")
        
        print("\n🎯 INSTRUCCIONES:")
        print("1. Ejecuta el script SQL en Supabase:")
        print("   - Ve a tu proyecto en https://supabase.com")
        print("   - Ve a SQL Editor")
        print("   - Pega el contenido de create_email_logs_table.sql")
        print("   - Ejecuta el script")
        print()
        print("2. Ejecuta python app.py y prueba enviar emails")
        print("3. Ve el historial con la opción 3 del menú")
        
    except Exception as e:
        if "relation \"email_logs\" does not exist" in str(e):
            print("⚠️  La tabla email_logs no existe todavía")
            print("📋 Necesitas ejecutar el script SQL en Supabase")
        else:
            print(f"❌ Error: {e}")

if __name__ == "__main__":
    test_email_logs()