import pandas as pd
from habitacion import Habitacion
from validaciones import Validaciones


class RepositorioHabitaciones:
    def __init__(self, ruta):
        self.ruta = ruta

    def cargar(self):
        df = pd.read_excel(self.ruta, dtype={"NRO": str})
        habitaciones = []
        for _, fila in df.iterrows():
            nueva = Habitacion(fila["NRO"], fila["TIPO"], fila["PRECIO"], fila["ESTADO"], fila["VISITAS"], fila["DINERO_GENERADO"])
            habitaciones.append(nueva)
        return habitaciones
    
    def guardar(self, lista_habitaciones):
        data = []
        for h in lista_habitaciones:
            data.append(h.to_dict())
        df = pd.DataFrame(data)
        df.to_excel(self.ruta, index=False)

class GestorHabitaciones:
    def __init__(self, repositorio, habitaciones):
        self.repo = repositorio
        self.lista_habitaciones = habitaciones
    
    def registrar_habitacion(self):
        nro = Validaciones.ingresar_cadena(3,3, "N° de habitación: ",2)
        hab = next((h for h in self.lista_habitaciones if h.nro == nro), None)
        if hab is not None:
            print("La habitación ya ha sido registrada!")
            return
        op_tipo = Validaciones.ingresar_numero(1,4, "Tipo:\n1. Simple\n2. Familiar\n3. Matrimonial\n4. Jacuzzi\nOpción: ")
        match op_tipo:
            case 1: tipo = "simple"
            case 2: tipo = "familiar"
            case 3: tipo = "matrimonial"
            case 4: tipo = "jacuzzi"
        precio = Validaciones.ingresar_numero(30,200, "Precio (S/): ")
        nueva_habitacion = Habitacion(nro, tipo, precio)
        self.lista_habitaciones.append(nueva_habitacion)
        self.repo.guardar(self.lista_habitaciones)
        print(f"Nueva habitación registrada con éxito!")

    def mostrar_lista(self):
        if not self.lista_habitaciones:
            print("No hay habitaciones para mostrar.")
            return
        print(f"{'#':<5}{'N° HAB':<10}{'TIPO':<15}{'PRECIO':<10}{'ESTADO':<15}{'VISITAS':<15}{'INGRESO S/':<15}")
        for i, h in enumerate(self.lista_habitaciones, start = 1):
            print(f"{i}.   {h}")

    def buscar_habitacion(self):
        nro = Validaciones.ingresar_cadena(3,3, "N° de habitación a buscar: ", 2)
        habitacion = next((h for h in self.lista_habitaciones if h.nro == nro), None)
        if habitacion is None:
            print("Habitacíon no registrada!")
            return
        habitacion.info()