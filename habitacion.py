class Habitacion:
    def __init__(self, nro, tipo, precio, estado="disponible", visitas=0, dinero_generado=0):
        self.nro = nro
        self.tipo = tipo
        self.precio = precio
        self.estado = estado
        self.visitas = visitas
        self.dinero_generado = dinero_generado

    def to_dict(self):
        return {
            "NRO": self.nro,
            "TIPO": self.tipo,
            "PRECIO": self.precio,
            "ESTADO": self.estado,
            "VISITAS": self.visitas,
            "DINERO_GENERADO": self.dinero_generado
        }
    
    def info(self):
        print("\n[=== Acerca de la habitación ===]")
        print(f"- Nro: {self.nro}")
        print(f"- Tipo: {self.tipo}")
        print(f"- Precio: S/{self.precio:02f}")
        print(f"- Estado: {self.estado.capitalize()}")
        print(f"- Total de visitas: {self.visitas}")
        print(f"- Dinero generado: S/{self.dinero_generado}")


    def __str__(self):
        return f"{self.nro:<10}{self.tipo:<15}{self.precio:<10}{self.estado:<15}{self.visitas:<15}{self.dinero_generado:<15}"


    

    