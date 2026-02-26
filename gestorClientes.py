from validaciones import Validaciones
from clientes import Cliente
import pandas as pd
from interfaz import Interfaz

class RepositorioCliente:
    def __init__(self, ruta):
        self.ruta = ruta

    def cargar(self): #Convierte cada fila del df a un objeto cliente y retorna la lista completa
        df = pd.read_excel(self.ruta, dtype={"DNI": str, "CELULAR": str})
        clientes = []
        for _, fila in df.iterrows():
            nuevo = Cliente(fila["NOMBRES"], fila["A. PATERNO"], fila["A. MATERNO"], fila["DNI"],
                            fila["EDAD"], fila["SEXO"], fila["CELULAR"], fila["CORREO"], fila["ENTRADAS"],
                            fila["C. ENTRADAS"], fila["C. CANTINA"])
            clientes.append(nuevo)
        return clientes
    
    def guardar(self, lista_clientes): #Guarda la lista de clientes como un nuevo df
        data = []
        for c in lista_clientes:
            data.append(c.to_dict())
        df = pd.DataFrame(data)
        df.to_excel(self.ruta, index=False)

class GestorClientes:
    def __init__(self, repositorio, clientes):
        self.repo = repositorio
        self.lista_clientes = clientes

    def registrar_cliente(self):
        dni = Validaciones.ingresar_cadena(8,8, "DNI del nuevo cliente: ", 2)
        for c in self.lista_clientes:
            if c.dni == dni:
                print(f"El DNI ya ha sido registrado.")
        
        nombres = Validaciones.ingresar_cadena(3,50, "Nombres: ")
        a_paterno = Validaciones.ingresar_cadena(3,30, "Apellido paterno: ")
        a_materno = Validaciones.ingresar_cadena(3,30, "Apellido materno: ")
        edad = Validaciones.ingresar_numero(18, 100, "Edad: ")
        op = Validaciones.ingresar_numero(1,2, "Sexo:\n1. Masculino\n2. Femenino\nOpcion: ")
        sexo = "M" if op == 1 else "F"
        celular = Validaciones.ingresar_cadena(9,9, "N° de celular: ", 2)
        op_correo = Validaciones.ingresar_numero(1,2, "Desea agregar un correo electrónico? (1. Si/2. No): ")
        if op_correo == 1:
            correo = Validaciones.ingresar_correo("Correo: ")
        else:
            correo = "-"
        
        nuevo_cliente = Cliente(nombres, a_paterno, a_materno, dni, edad, sexo, celular, correo)
        self.lista_clientes.append(nuevo_cliente)
        self.repo.guardar(self.lista_clientes)
        print("Cliente registrado con éxito!")

    def mostrar_lista(self):
        if not self.lista_clientes:
            Interfaz.mensaje_info("No hay clientes para mostrar.")
            return
        
        # Definimos las columnas
        columnas = ["#", "Cliente", "DNI", "Edad", "Sexo", "Celular", "Total Gastado"]
        filas = []

        for i, c in enumerate(self.lista_clientes, start=1):
            # Preparamos la fila. Usamos colores condicionales si quieres
            sexo_icon = "♂️" if c.sexo == "M" else "♀️"
            estilo_gasto = f"[green]S/{c.consumo_total:.2f}[/green]"
            
            filas.append([
                i, 
                f"{c.nombres} {c.aPaterno}", 
                c.dni, 
                c.edad, 
                sexo_icon, 
                c.celular, 
                estilo_gasto
            ])

        Interfaz.mostrar_tabla("Directorio de Clientes", columnas, filas)
 
    def buscar(self):
        if not self.lista_clientes:
            print("No hay clientes para mostrar.")
            return
        
        dni_cliente = Validaciones.ingresar_cadena(8,8, "DNI del cliente: ", 2)
        cliente = next((c for c in self.lista_clientes if c.dni == dni_cliente), None)
        if cliente is None:
            print("Cliente no encontrado")
            return
        print()
        cliente.info()
        op = Validaciones.ingresar_numero(1,3, "¿Qué operación desea realizar?\n1. Consultar información adicional\n2. Modificar información\n3. Ver historial de entradas\n4. Volver\nOpción: ")
        if op == 1:
            if cliente.hab_favorita is not None:
                print(f"- Habitación Favorita: {cliente.hab_favorita}")
            cliente.info_hab_especifica(cliente.hab_favorita)
        elif op == 2:
            dic_cliente = cliente.to_dict()
            for k,v in dic_cliente.items():
                print(f"- {k}: {v}")

            mod = Validaciones.ingresar_numero(1,11, "Seleccione la información que desea modificar:\n1. Nombres | 2. A. Paterno | 3. A. Materno\n4. DNI | 5. Edad | 6. Sexo\n7. Celular | 8. Correo | 9. Entradas\n10. C. Entradas | 11. C. Cantina\nOpción: ")
            match mod:
                case 1: 
                    nuevo = Validaciones.ingresar_cadena(3,50, "Nuevos nombres: ")
                    cliente.nombres = nuevo
                case 2:
                    nuevo = Validaciones.ingresar_cadena(3,30, "Nuevo apellido paterno: ")
                    cliente.aPaterno = nuevo
                case 3:
                    nuevo = Validaciones.ingresar_cadena(3,30, "Nuevo apellido materno: ")
                    cliente.aMaterno = nuevo 
                case 4:
                    nuevo = Validaciones.ingresar_cadena(8,8, "Nuevo DNI: ", 2)
                    cliente.dni = nuevo
                case 5:
                    nuevo = Validaciones.ingresar_numero(5,100, "Nueva edad: ")
                    cliente.edad = nuevo
                case 6:
                    op = Validaciones.ingresar_numero(1,2, "Nuevo sexo:\n1. Masculino\n2. Femenino\nOpción: ")
                    nuevo = "M" if op == 1 else "F"
                    cliente.sexo = nuevo
                case 7:
                    nuevo = Validaciones.ingresar_cadena(9,9, "Nuevo celular: ", 2)
                    cliente.celular = nuevo
                case 8:
                    nuevo = Validaciones.ingresar_correo("Nuevo correo electrónico: ")
                    cliente.correo = nuevo
                case 9:
                    nuevo = Validaciones.ingresar_numero(0,100, "Nuevo N° de entradas: ")
                    cliente.entradas = nuevo
                case 10:
                    nuevo = Validaciones.ingresar_numero(0, 5000, "Nuevo consumo de entradas S/: ")
                    cliente.c_entradas = nuevo
                case 11:
                    nuevo = Validaciones.ingresar_numero(0, 5000, "Nuevo consumo de cantina S/: ")
                    cliente.c_cantina = nuevo
            self.repo.guardar(self.lista_clientes)
            print("Información actualizada con éxito! ")
        elif op == 3:
            return
        
    def ver_ranking(self):
        if not self.lista_clientes:
            print("No hay clientes para mostrar.")
            return
        print("[=== Ranking de mejores clientes ===]")
        print(f"\n{'#':<5}{'Cliente':<35}{'DNI':<15}{'Entradas':<15}{'C. Entradas':<15}{'C. Cantina':<15}{'C. Total':<15}")
        print(f"-"*115)
        ordenados = sorted(self.lista_clientes, key=lambda x: x.consumo_total, reverse=True)
        for i, c in enumerate(ordenados, start=1):
            if i == 1:
                i = "🥇"
            elif i == 2:
                i = "🥈"
            elif i == 3:
                i = "🥉"
            else:
                i = str(i) + "."
            nom_completo = (f"{c.nombres} {c.aPaterno} {c.aMaterno}").title()
            print(
                f"{i}   "
                f"{nom_completo:<35}"
                f"{c.dni:<15}"
                f"{c.entradas:<15}"
                f"{c.c_entradas:<15}"
                f"{c.c_cantina:<15}"
                f"{c.consumo_total:<15}"
            )