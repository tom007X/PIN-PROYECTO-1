import pytest
from app import app  # Importa tu aplicación Flask


@pytest.fixture
def client():
    """Configura el cliente de pruebas para la app de Flask."""
    app.config['TESTING'] = True
    with app.test_client() as client:
        yield client


def test_health_check(client):
    """Verifica el endpoint raíz (health check)."""
    response = client.get('/')
    assert response.status_code == 200
    data = response.get_json()
    assert data['status'] == 'ok'
    assert data['servicio'] == 'api-clientes'


def test_listar_clientes_vacio(client):
    """Verifica que al inicio la lista de clientes esté vacía."""
    response = client.get('/clientes')
    assert response.status_code == 200
    assert response.get_json() == []


def test_crear_cliente(client):
    """Verifica la creación exitosa de un cliente."""
    nuevo_cliente = {
        "nombre": "Nicolás",
        "email": "nicolas@example.com",
        "dni": "12345678"
    }
    response = client.post('/clientes', json=nuevo_cliente)
    assert response.status_code == 201
    data = response.get_json()
    assert data['id'] == 1
    assert data['nombre'] == "Nicolás"
    assert data['email'] == "nicolas@example.com"
    assert data['dni'] == "12345678"


def test_crear_cliente_faltan_campos(client):
    """Verifica que falle si faltan campos obligatorios como el email."""
    cliente_incompleto = {
        "nombre": "Carlos"
        # falta email
    }
    response = client.post('/clientes', json=cliente_incompleto)
    assert response.status_code == 400
    data = response.get_json()
    assert 'error' in data


def test_obtener_cliente_por_id(client):
    """Verifica la obtención de un cliente existente por su ID."""
    # Primero aseguramos que exista al menos uno (ID 1 creado en tests anteriores o creamos uno nuevo)
    response_get = client.get('/clientes/1')
    assert response_get.status_code == 200
    data = response_get.get_json()
    assert data['id'] == 1


def test_obtener_cliente_no_encontrado(client):
    """Verifica que devuelva 404 si el cliente no existe."""
    response = client.get('/clientes/999')
    assert response.status_code == 404
    data = response.get_json()
    assert data['error'] == 'Cliente no encontrado'


def test_actualizar_cliente(client):
    """Verifica la actualización de los datos de un cliente."""
    datos_actualizados = {
        "nombre": "Nicolás Actualizado",
        "email": "nicolas.nuevo@example.com",
        "dni": "87654321"
    }
    response = client.put('/clientes/1', json=datos_actualizados)
    assert response.status_code == 200
    data = response.get_json()
    assert data['nombre'] == "Nicolás Actualizado"
    assert data['email'] == "nicolas.nuevo@example.com"


def test_borrar_cliente(client):
    """Verifica la eliminación de un cliente."""
    response = client.delete('/clientes/1')
    assert response.status_code == 204

    # Verificar que ya no existe
    response_get = client.get('/clientes/1')
    assert response_get.status_code == 404