"""
Configuración básica para tests simples
"""
import os
import sys
import pytest
from unittest.mock import Mock

# Agregar el directorio raíz al path
project_root = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
if project_root not in sys.path:
    sys.path.insert(0, project_root)

from app import app

@pytest.fixture
def client():
    """Cliente de test para Flask"""
    app.config['TESTING'] = True
    with app.test_client() as client:
        yield client

@pytest.fixture
def mock_supabase():
    """Mock simple de Supabase"""
    mock = Mock()
    mock.table.return_value.select.return_value.eq.return_value.execute.return_value.data = []
    mock.table.return_value.insert.return_value.execute.return_value.data = [{'id': 1}]
    return mock