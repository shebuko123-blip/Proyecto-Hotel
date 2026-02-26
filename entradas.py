class Entrada:
    def __init__(self, cliente, habitacion, hora_ingreso, pago, metodo, fecha_turno, hora_salida="-"):
        self.cliente = cliente
        self.habitacion = habitacion
        self.hora_ingreso = hora_ingreso
        self.hora_salida = hora_salida
        self.pago = pago
        self.metodo = metodo
        self.fecha_turno = fecha_turno

    def to_dict(self):
        return {
            "NRO_HABITACION": self.habitacion.nro,
            "DNI_CLIENTE":self.cliente.dni,
            "NOMBRE_CLIENTE": f"{self.cliente.nombres} {self.cliente.aPaterno} {self.cliente.aMaterno}",
            "INGRESO": self.hora_ingreso,
            "SALIDA": self.hora_salida,
            "PAGO": self.pago,
            "METODO": self.metodo,
            "FECHA_TURNO": self.fecha_turno
        }
    
    def info(self):
        nombre_completo = (f"{self.cliente.nombres} {self.cliente.aPaterno} {self.cliente.aMaterno}").title()
        print(f"Nro. Habitación: {self.habitacion.nro}")
        print(f"DNI cliente: {self.cliente.dni}")
        print(f"Nombre cliente: {nombre_completo}")
        print(f"Hora de ingreso: {self.hora_ingreso}")
        print(f"Hora de salida: {self.hora_salida}")
        print(f"Pago (S/): {self.pago:<2f}")
        print(f"Método de pago: {self.metodo}")
        print(f"Fecha: {self.fecha_turno}")
    
    def __str__(self):
        nombre_completo = (f"{self.cliente.nombres} {self.cliente.aPaterno} {self.cliente.aMaterno}").title()
        return f"{self.habitacion.nro:<10}{nombre_completo:<35}{self.cliente.dni:<15}{self.hora_ingreso:<12}{self.hora_salida:<12}{self.pago:<10}{self.metodo:<12}{self.fecha_turno:<15}"