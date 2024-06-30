const database = 'sistemaventas';

// Use the database.
use(database);

// Crear la primera coleccion.
db.createCollection('producto');

// Crear la segunda coleccion.
db.createCollection('cliente');