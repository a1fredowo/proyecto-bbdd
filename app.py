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
    query = {}
    if categoria:
        query['categoria'] = categoria
    if marca:
        query['marca'] = marca
    
    productos = list(db.producto.find(query))
    for producto in productos:
        producto['_id'] = str(producto['_id'])  # Convertir ObjectId a string
    
    return jsonify(productos), 200

@app.route('/delete_all_products', methods=['DELETE'])
def delete_all_products():
    result = db.producto.delete_many({})
    return jsonify({'msg': f'{result.deleted_count} productos eliminados.'}), 200

@app.route('/fetch_and_store', methods=['GET'])
def fetch_and_store():
    # Obtener submissions de form.io
    response = requests.get(form_io_submissions_url)
    submissions = response.json()

    # Insertar submissions en MongoDB
    for submission in submissions:
        db.producto.insert_one(submission['data'])

    return jsonify({'msg': f"{len(submissions)} submissions insertadas en MongoDB."}), 201

@app.route('/view_products', methods=['GET'])
def view_products():
    productos = list(db.producto.find())
    for producto in productos:
        producto['_id'] = str(producto['_id'])  # Convertir ObjectId a string
    return render_template('index.html', productos=productos)

if __name__ == '__main__':
    app.run(debug=True)
