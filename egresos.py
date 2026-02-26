import pandas as pd
from validaciones import Validaciones

class Egreso:
    def __init__(self, detalle, monto, categoria, fecha):
        self.detalle = detalle
        self.monto = monto
        self.categoria = categoria
        self.fecha = fecha

    def to_dict(self):
        return {
            "DETALLE": self.detalle,
            "MONTO": self.monto,
            "CATEGORIA": self.categoria,
            "FECHA": self.fecha
        }
    
    def __str__(self):
        return f"{self.detalle:<20}{self.monto:<15}{self.categoria:<15}{self.fecha:<15}"

class RepositorioEgresos:
    def __init__(self, ruta):
        self.ruta = ruta
    
    def cargar(self):
        df = pd.read_excel(self.ruta)
        lista = []
        for _, fila in df.iterrows():
            nuevo = Egreso(fila["DETALLE"], fila["MONTO"], fila["CATEGORIA"], fila["FECHA"])
            lista.append(nuevo)
        return lista
    
    def guardar(self, lista_egresos):
        data = []
        for e in lista_egresos:
            data.append(e.to_dict())
        df = pd.DataFrame(data)
        df.to_excel(self.ruta, index=False)

class GestorEgresos:
    def __init__(self, repositorio:RepositorioEgresos):
        self.repo = repositorio
        self.lista_egresos = self.repo.cargar()

    def elegir_categoria(self):
        categorias = ["Cantina", "Operativos", "Fijos", "Mantenimiento", "Personal y varios"]
        print("Categorías de los gastos: ")
        for i, c in enumerate(categorias, start=1):
            print(f"{i}. {c}")
        op = Validaciones.ingresar_numero(1, len(categorias), "Opcion: ") -1
        return categorias[op]


    def registrar_egreso(self):
        detalle = Validaciones.ingresar_cadena(3,30, "Detalle del gasto: ")
        monto = Validaciones.ingresar_numero(1,10000, "Monto (S/): ", False)
        categoria = self.elegir_categoria()
        
        ahora = pd.Timestamp.now()
        if ahora.hour < 8:
            fecha = (ahora - pd.Timedelta(days=1)).strftime("%d-%m-%Y")
        else:
            fecha = ahora.strftime("%d-%m-%Y")

        nuevo_egreso = Egreso(detalle, monto, categoria, fecha)
        self.lista_egresos.append(nuevo_egreso)
        self.repo.guardar(self.lista_egresos)
        print("\nGasto registrado con éxito!")

    def mostrar_lista(self):
        if not self.lista_egresos:
            print("No hay egresos para mostrar.")
            return

        print(f"{'N°':<5}{'DETALLE':<20}{'MONTO S/':<15}{'CATEGORIA':<15}{'FECHA':<15}")
        print(f"-"*70)
        for i, e in enumerate(self.lista_egresos, start=1):
            print(f"{i}.   {e}")
        
        print("\n[=== RESUMEN GENERAL DE EGRESOS ===]")
        total = [e.monto for e in self.lista_egresos].sum()
        print(f"Dinero total gastado: S/{total:.2f}")
        print(f"Categoría ")

        