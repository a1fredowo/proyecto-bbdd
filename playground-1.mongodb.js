const database = 'sistemaventas';

use(database);

db.createCollection('producto');
db.createCollection('cliente');
db.createCollection('pedido');
db.createCollection('proveedor');
db.createCollection('transbank');
db.createCollection('venta');
db.createCollection('facturacion');
db.createCollection('detalle_pedido');