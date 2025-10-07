"""
4 Tests simples que funcionan
"""
import json
from unittest.mock import patch

def test_health_endpoint(client):
    """Test 1: El endpoint de salud funciona"""
    response = client.get('/health')
    assert response.status_code == 200
    data = json.loads(response.data)
    assert data['estado'] == 'ok'

def test_registration_missing_data(client):
    """Test 2: Registro sin datos retorna error 400"""
    response = client.post('/registro', 
                         data='{}',
                         content_type='application/json')
    assert response.status_code == 400

def test_login_missing_data(client):
    """Test 3: Login sin datos retorna error 400"""
    response = client.post('/login',
                         data='{}', 
                         content_type='application/json')
    assert response.status_code == 400

def test_protected_endpoint_without_token(client):
    """Test 4: Endpoint protegido sin token retorna 401"""
    response = client.get('/perfil')
    assert response.status_code == 401
    data = json.loads(response.data)
    assert 'Token requerido' in data['error']