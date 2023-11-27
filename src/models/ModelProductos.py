from .entities.productos import Producto  # Importa la clase Producto desde entities

class ModelProductos():
    @classmethod
    def obtener_todos(cls, db):
        try:
            cursor = db.connection.cursor()
            cursor.execute("SELECT id, nombre, imagen, precio FROM productos")
            rows = cursor.fetchall()

            productos = []
            for row in rows:
                producto = Producto(row[0], row[1], row[2], row[3])
                productos.append(producto)

            return productos
        except Exception as ex:
            raise Exception(ex)
