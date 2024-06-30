import requests
from faker import Faker
import random

# URL de la API de form.io para realizar submissions
form_io_url = 'https://csdpmqimmmrbnbp.form.io/producto/submission'  # Reemplaza con la URL de tu formulario en form.io

# Inicializar Faker
fake = Faker()

# Opciones para los campos específicos
categorias = ['Motos', 'Repuestos', 'Accesorios']
marcas = ['Honda', 'Bajaj', 'Suzuki', 'Yamaha', 'Kawasaki', 'BMW', 'Ducati', 'Harley-Davidson', 'Triumph', 'KTM']
nombres = {
    'Motos': ['Moto', 'Motocicleta', 'Scooter'],
    'Repuestos': ['Cadenas', 'Baterías', 'Repuestos'],
    'Accesorios': ['Casco', 'Chaqueta', 'Guante']
}

# Generar datos ficticios
def generar_datos_ficticios(n, start_id):
    datos = []
    id_producto = start_id
    for _ in range(n):
        categoria = random.choice(categorias)
        nombre_producto = f"{random.choice(nombres[categoria])} {fake.word()}"
        descripcion = fake.text(max_nb_chars=200)  # Descripción más larga
        stock = random.randint(3, 100)
        if categoria == 'Motos':
            precio = round(random.uniform(1000000, 2000000), 2)
        else:
            precio = round(random.uniform(10000, 100000), 2)

        producto = {
            "data": {
                "idProducto": id_producto,  # ID Producto incremental
                "nombre": nombre_producto,
                "sku": fake.bothify(text='SKU###??'),
                "descripcion": descripcion,
                "precio": precio,
                "categoria": categoria,
                "marca": random.choice(marcas),
                "stock": stock
            }
        }
        datos.append(producto)
        id_producto += 1  # Incrementar el ID Producto
    return datos

# Obtener el número actual de submissions para empezar el ID correctamente
def obtener_siguiente_id(form_io_submissions_url):
    response = requests.get(form_io_submissions_url)
    submissions = response.json()
    if submissions:
        max_id = max(submission['data']['idProducto'] for submission in submissions)
        return max_id + 1
    return 1

# URL de la API de form.io para obtener submissions
form_io_submissions_url = 'https://csdpmqimmmrbnbp.form.io/producto/submission'

# Obtener el siguiente ID
siguiente_id = obtener_siguiente_id(form_io_submissions_url)

# Número de datos ficticios a generar
num_datos = 500

# Obtener los datos ficticios
datos_ficticios = generar_datos_ficticios(num_datos, siguiente_id)

# Realizar submissions a form.io
for data in datos_ficticios:
    response = requests.post(form_io_url, json=data)
    if response.status_code == 201:
        print(f"Submission successful: {response.json()}")
    else:
        print(f"Submission failed: {response.status_code} - {response.text}")
