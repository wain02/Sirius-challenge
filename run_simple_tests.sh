"""
Script para ejecutar los tests simples
"""
#!/bin/bash

echo "🚀 Ejecutando tests simples del Email Service"
echo "============================================="

# Activar el entorno virtual si existe
if [ -d "venv" ]; then
    source venv/bin/activate
    echo "✅ Entorno virtual activado"
fi

# Ejecutar los tests
echo "📋 Ejecutando tests..."
python -m pytest tests/test_simple.py -v

echo ""
echo "✨ Tests completados!"