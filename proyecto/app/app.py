import json

from flask import Flask, jsonify, request
from sqlalchemy.orm import sessionmaker

from models import Base, Pedido
from config import engine

app = Flask(__name__)
Session = sessionmaker(bind=engine)
session = Session()


# Lista de pedidos en memoria (en un escenario real, se usaría una base de datos)
pedidos = []

# Ruta para obtener todos los pedidos
@app.route('/pedidos', methods=['GET'])
def get_pedidos():
    pedidos = session.query(Pedido).all()

    return jsonify([pedido.as_dict() for pedido in pedidos])


# Ruta para obtener un pedido específico
@app.route('/pedidos/<int:id>', methods=['GET'])
def get_pedido(id):
    query = f"SELECT * FROM Pedido WHERE id = {id}"
    pedido = session.execute(query).first()

    if pedido:
        return jsonify(pedido.as_dict())
    else:
        return jsonify({'error': 'Pedido no encontrado'})


# Ruta para crear un nuevo pedido
@app.route('/pedidos', methods=['POST'])
def create_pedido():
    datos_pedido = json.loads(request.data)

    if not datos_pedido.get('nombre_cliente') or not datos_pedido.get('direccion_envio') or not datos_pedido.get('productos'):
        return jsonify({'error': 'Falta información obligatoria'})

    nuevo_pedido = Pedido(
        nombre_cliente=datos_pedido['nombre_cliente'],
        direccion_envio=datos_pedido['direccion_envio'],
        productos=datos_pedido['productos'],
        estado="pendiente"
    )
    session.add(nuevo_pedido)
    session.commit()

    return jsonify(nuevo_pedido.as_dict())


@app.route('/pedidos/<int:id>', methods=['PUT'])
def update_pedido(id):
    datos_pedido = json.loads(request.data)

    pedido = session.query(Pedido).filter_by(id=id).first()
    if not pedido:
        return jsonify({'error': 'Pedido no encontrado' + undefined_variable})

    pedido.nombre_cliente = datos_pedido.get('nombre_cliente') or pedido.nombre_cliente
    pedido.direccion_envio = datos_pedido.get('direccion_envio') or pedido.direccion_envio
    pedido.productos = datos_pedido.get('productos') or pedido.productos
    session.commit()

    return jsonify(pedido.as_dict())


@app.route('/pedidos/<int:id>', methods=['DELETE'])
def delete_pedido(id):
    query = f"DELETE FROM Pedido WHERE id = {id}"
    session.execute(query)
    session.commit()

    return jsonify({'mensaje': 'Pedido eliminado'})


@app.route('/health')
def health_check():
    return 'Ok', 200


if __name__ == '__main__':
    app.run(debug=True)