import os
from app import app
from flask import jsonify, request
from prometheus_flask_exporter import PrometheusMetrics


# ============================================================
# Métricas Prometheus
# ============================================================
# Expone automáticamente métricas en /metrics
metrics = PrometheusMetrics(app)
# ==================================
# ==========================
# Almacenamiento en memoria
# ============================================================
# Estructura: {id: {"id": int, "nombre": str, "email": str, "dni": str|None}}
_clientes = {}
_next_id = 1


def _nuevo_id():
    """Genera un ID incremental para el próximo cliente."""
    global _next_id
    nuevo = _next_id
    _next_id += 1
    return nuevo


# ============================================================
# Endpoints
# ============================================================

@app.route('/', methods=['GET'])
def health():
    return jsonify({'status': 'ok', 'servicio': 'api-clientes'}), 200


@app.route('/clientes', methods=['GET'])
def listar_clientes():
    # Devolvemos una lista con todos los clientes almacenados en memoria
    return jsonify(list(_clientes.values())), 200


@app.route('/clientes/<int:id>', methods=['GET'])
def obtener_cliente(id):
    cliente = _clientes.get(id)
    if not cliente:
        return jsonify({'error': 'Cliente no encontrado'}), 404
    return jsonify(cliente), 200


@app.route('/clientes', methods=['POST'])
def crear_cliente():
    try:
        data = request.get_json()
        if not data:
            return jsonify({'error': 'Cuerpo JSON requerido'}), 400

        nombre = data.get('nombre')
        email = data.get('email')
        dni = data.get('dni')

        if not nombre or not email:
            return jsonify({'error': 'Los campos nombre y email son obligatorios'}), 400

        nuevo_id = _nuevo_id()
        cliente = {
            'id': nuevo_id,
            'nombre': nombre,
            'email': email,
            'dni': dni,
        }
        _clientes[nuevo_id] = cliente
        return jsonify(cliente), 201
    except Exception as e:
        print(e)
        return jsonify({'error': 'Error al crear el cliente'}), 500


@app.route('/clientes/<int:id>', methods=['PUT'])
def actualizar_cliente(id):
    try:
        if id not in _clientes:
            return jsonify({'error': 'Cliente no encontrado'}), 404

        data = request.get_json()
        if not data:
            return jsonify({'error': 'Cuerpo JSON requerido'}), 400

        nombre = data.get('nombre')
        email = data.get('email')
        dni = data.get('dni')

        if not nombre or not email:
            return jsonify({'error': 'Los campos nombre y email son obligatorios'}), 400

        cliente = {
            'id': id,
            'nombre': nombre,
            'email': email,
            'dni': dni,
        }
        _clientes[id] = cliente
        return jsonify(cliente), 200
    except Exception as e:
        print(e)
        return jsonify({'error': 'Error al actualizar el cliente'}), 500


@app.route('/clientes/<int:id>', methods=['DELETE'])
def borrar_cliente(id):
    try:
        if id not in _clientes:
            return jsonify({'error': 'Cliente no encontrado'}), 404
        del _clientes[id]
        return '', 204
    except Exception as e:
        print(e)
        return jsonify({'error': 'Error al borrar el cliente'}), 500



if __name__ == "__main__":
    app.run(host='0.0.0.0', port=int(os.environ.get('PORT', 8080)))
    