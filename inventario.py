class Producto:
    def __init__(self, codigo, nombre, categoria, precio, stock, total_vendido=0, total_generado=0):
        self.codigo = codigo
        self.nombre = nombre
        self.categoria = categoria
        self.precio = precio
        self.stock = stock
        self.total_vendido = total_vendido
        self.total_generado = total_generado

    def to_dict(self):
        return {
            "CODIGO": self.codigo,
            "NOMBRE": self.nombre,
            "CATEGORIA": self.categoria,
            "PRECIO": self.precio,
            "STOCK": self.stock,
            "VENDIDO": self.total_vendido,
            "GENERADO": self.total_generado
        }

    def __str__(self):
        return f"{self.codigo:<10}{self.nombre:<20}{self.categoria:<15}{self.precio:<12}{self.stock:<10}{self.total_vendido:<15}{self.total_generado:<12}"
    
class VentaCantina:
    def __init__(self, producto, cliente, cantidad, fecha):
        self.producto = producto
        self.cliente = cliente
        self.cantidad = cantidad
        self.fecha = fecha

    @property
    def pago(self):
        return self.producto.precio * self.cantidad
    def __str__(self):
        return f"{self.producto.nombre.capitalize():<20}{self.producto.codigo:<10}{(f"{self.cliente.nombres} {self.cliente.aPaterno} {self.cliente.aMaterno}").title():<35}{self.cliente.dni:<15}{self.cantidad:<12}{self.pago:<12}{self.fecha:<15}"
    def to_dict(self):
        return {
            "CODIGO": self.producto.codigo,
            "NOMBRE": self.producto.nombre,
            "DNI_CLIENTE": self.cliente.dni,
            "NOMBRE_CLIENTE": (f"{self.cliente.nombres} {self.cliente.aPaterno} {self.cliente.aMaterno}"),
            "CANTIDAD": self.cantidad,
            "PAGO": self.pago,
            "FECHA": self.fecha
        }