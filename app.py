from flask import Flask, request, jsonify, render_template
from pymongo import MongoClient
import requests
from bson import ObjectId

app = Flask(__name__)

# Conexión a MongoDB
client = MongoClient('mongodb://localhost:27017/')
db = client['sistemaventas']

# URL de la API de form.io para obtener submissions
form_io_submissions_url = 'https://csdpmqimmmrbnbp.form.io/producto/submission'

@app.route('/add_product', methods=['POST'])
def add_product():
    data = request.json
    db.producto.insert_one(data)
    return jsonify({'msg': 'Producto agregado exitosamente'}), 201

@app.route('/get_products', methods=['GET'])
def get_products():
    # Obtener parámetros de filtrado de la consulta
    categoria = request.args.get('categoria')
    marca = request.args.get('marca')
    ordenar = request.args.get('ordenar', 'idProducto')
    orden = request.args.get('orden', 'asc')
    query = {}
    if categoria:
        query['categoria'] = categoria
    if marca:
        query['marca'] = marca

    # Determinar el orden de ordenación
    sort_order = 1 if orden == 'asc' else -1

    productos = list(db.producto.find(query).sort(ordenar, sort_order))
    for producto in productos:
        producto['_id'] = str(producto['_id'])  # Convertir ObjectId a string

    return jsonify(productos), 200

@app.route('/delete_all_products', methods=['DELETE'])
def delete_all_products():
    result = db.producto.delete_many({})
    return jsonify({'msg': f'{result.deleted_count} productos eliminados.'}), 200

@app.route('/fetch_and_store', methods=['GET'])
def fetch_and_store():
    # Obtener submissions de form.io con limitación y paginación
    limit = 500  # Número de submissions a obtener
    skip = 0  # Se puede incrementar para paginación
    params = {'limit': limit, 'skip': skip}
    response = requests.get(form_io_submissions_url, params=params)
    submissions = response.json()

    # Insertar submissions en MongoDB evitando duplicados
    nuevos_productos = 0
    for submission in submissions:
        producto = submission['data']
        if not db.producto.find_one({'idProducto': producto['idProducto']}):
            db.producto.insert_one(producto)
            nuevos_productos += 1

    return jsonify({'msg': f'{nuevos_productos} nuevos productos insertados en MongoDB.'}), 201

@app.route('/view_products', methods=['GET'])
def view_products():
    # Obtener parámetros de filtrado de la consulta
    categoria = request.args.get('categoria')
    marca = request.args.get('marca')
    ordenar = request.args.get('ordenar', 'idProducto')
    orden = request.args.get('orden', 'asc')
    query = {}
    if categoria:
        query['categoria'] = categoria
    if marca:
        query['marca'] = marca

    # Determinar el orden de ordenación
    sort_order = 1 if orden == 'asc' else -1

    productos = list(db.producto.find(query).sort(ordenar, sort_order))
    for producto in productos:
        producto['_id'] = str(producto['_id'])  # Convertir ObjectId a string

    return render_template('index.html', productos=productos)

if __name__ == '__main__':
    app.run(debug=True)
