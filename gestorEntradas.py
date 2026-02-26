import pandas as pd
from entradas import Entrada
from validaciones import Validaciones
import msvcrt 


class RepositorioEntradas:
    def __init__(self, ruta):
        self.ruta = ruta

    def cargar(self, lista_clientes, lista_habitaciones):
        df = pd.read_excel(self.ruta, dtype={"DNI_CLIENTE":str, "NRO_HABITACION":str, "INGRESO":str, "SALIDA":str})
        entradas = []
        for _, fila in df.iterrows():
            nro_hab = fila["NRO_HABITACION"]
            dni_en_fila = fila["DNI_CLIENTE"]
            

            cliente = next((c for c in lista_clientes if c.dni == dni_en_fila), None)
            habitacion = next((h for h in lista_habitaciones if h.nro == nro_hab), None)

            if not cliente or not habitacion:
                continue

            salida_val = fila["SALIDA"] if pd.notna(fila["SALIDA"]) else "-"

            nueva = Entrada(cliente, habitacion, fila["INGRESO"], 
                            fila["PAGO"], fila["METODO"], salida_val)
            entradas.append(nueva)
        return entradas
    
    def guardar(self, lista_entradas):
        data = []
        for e in lista_entradas:
            data.append(e.to_dict())
        df = pd.DataFrame(data)
        df.to_excel(self.ruta, index=False)


class GestorEntradas:
    def __init__(self, repo_e:RepositorioEntradas, repo_c, repo_h, lista_clientes, lista_habitaciones):
        self.repo = repo_e
        self.repo_clientes = repo_c
        self.repo_habitaciones = repo_h
        self.lista_clientes = lista_clientes
        self.lista_habitaciones = lista_habitaciones
        datos_cargados = self.repo.cargar(lista_clientes, lista_habitaciones)
        self.lista_entradas = datos_cargados if datos_cargados is not None else []

    def registrar_entrada(self):
        nro_hab = Validaciones.ingresar_cadena(3,3, "N° de habitación: ",2)
        habitacion = next((h for h in self.lista_habitaciones if h.nro == nro_hab), None)
        if habitacion is None:
            print("La habitacion no existe!")
            return
        if habitacion.estado != "disponible":
            print("La habitación no se encuentra disponible!")
            return
        dni_cliente = Validaciones.ingresar_cadena(8,8, "DNI del cliente: ", 2)
        cliente = next((c for c in self.lista_clientes if c.dni == dni_cliente), None)
        if not cliente:
            print("Cliente no registrado!")
            return
        if cliente.entrada_activa == True:
            print("El cliente ya cuenta con una entrada activa en estos momentos.")
            return
        
        pago = Validaciones.ingresar_numero(30,200, "Pago: ")
        op_metodo = Validaciones.ingresar_numero(1,4, "Método de pago:\n1. Efectivo\n2. Yape\n3. Plin\n4. Tarjeta\nOpcion: ")
        match op_metodo:
            case 1: metodo = "efectivo"
            case 2: metodo = "yape"
            case 3: metodo = "plin"
            case 4: metodo = "tarjeta"


        ahora = pd.Timestamp.now()
        ingreso = ahora.strftime("%H:%M")

        if ahora.hour < 8:
            fecha_turno = (ahora - pd.Timedelta(days=1)).strftime("%d-%m-%Y")
        else:
            fecha_turno = ahora.strftime("%d-%m-%Y")

        cliente.entradas+=1
        cliente.entrada_activa = True
        cliente.c_entradas += pago
        habitacion.estado = "ocupada"
        habitacion.visitas +=1
        habitacion.dinero_generado += pago

        datos_hab = []
        if nro_hab not in cliente.historial_hab:
            datos_hab = [1, pago]
        else:
            datos_hab = cliente.historial_hab[nro_hab]
            datos_hab[0] += 1
            datos_hab[1] += pago
        cliente.historial_hab[nro_hab] = datos_hab

        nueva_entrada = Entrada(cliente, habitacion, ingreso, pago, metodo , fecha_turno)
        self.lista_entradas.append(nueva_entrada)

        self.repo.guardar(self.lista_entradas)
        self.repo_clientes.guardar(self.lista_clientes)
        self.repo_habitaciones.guardar(self.lista_habitaciones)

        print("Entrada registrada exitosamente!")

    def mostrar_lista(self):
        if not self.lista_entradas:
            print("No hay entradas para mostrar.")
            return

        print(f"{'#':<5}{'N° HAB.':<10}{'CLIENTE':<35}{'DNI':<15}{'INGRESO':<12}{'SALIDA':<12}{'PAGO':<10}{'METODO':<12}{'FECHA':<15}")
        total_entradas = 0
        total_dinero = 0
        efectivo = 0
        cont_e = 0
        yape = 0
        cont_y = 0
        plin = 0
        cont_p = 0
        tarjeta = 0
        cont_t = 0
        for i, e in enumerate(self.lista_entradas, start = 1):
            total_entradas += 1
            total_dinero += e.pago
            if e.metodo == "efectivo": 
                efectivo+=e.pago
                cont_e+=1
            if e.metodo == "yape": 
                yape+=e.pago
                cont_y+=1
            if e.metodo == "plin": 
                plin+=e.pago
                cont_p+=1
            if e.metodo == "tarjeta": 
                tarjeta+=e.pago
                cont_t+=1

            print(f"{i}.   {e}")

        print("\n[=== Resumen general ===]")
        print(f"🚪 Total de entradas el día de hoy: {total_entradas} entradas.")
        print(f"💰 Total de dinero recaudado hoy: S/.{total_dinero}.")
        
        print("\n[=== Resumen por método de pago ===]")
        print(f"💸 EFECTIVO 💸")
        print(f"• Entradas: {cont_e} | • Dinero: {efectivo}")
        print(f"🟣 YAPE 🟣")
        print(f"• Entradas: {cont_y} | • Dinero: {yape}")
        print(f"🟢 PLIN 🟢")
        print(f"• Entradas: {cont_p} | • Dinero: {plin}")
        print(f"💳 TARJETA 💳")
        print(f"• Entradas: {cont_t} | • Dinero: {tarjeta}")
        
        

    def modificar_info(self):
        if not self.lista_entradas:
            print("No hay entradas registradas.")
            return
        
        dni_cliente = Validaciones.ingresar_cadena(8,8, "DNI del cliente: ",2)
        entrada_seleccionada = next((e for e in self.lista_entradas if e.cliente.dni == dni_cliente), None)

        if entrada_seleccionada is None:
            print("Ninguna entrada coincide con el DNI ingresado.")
            return
        else:
            cliente = entrada_seleccionada.cliente
            entrada_seleccionada.info()

        """
        op_mod = Validaciones.ingresar_numero(1,5, "Dato que desea modificar:\n1. DNI del cliente\n2. Hora ingreso\n3. Hora salida\n4. Pago\n5. Metodo\nOpcion: ")
        match op_mod:
            case 1:
                nuevo_dni = Validaciones.ingresar_cadena(8,8, "Nuevo DNI del cliente: ")
                cliente.dni = nuevo_dni
            case 2:
                nuevo_ingreso = Validaciones.ingresar_hora("Nueva hora de ingreso: ")
                entrada_seleccionada.hora_ingreso = nuevo_ingreso
            case 3:
                nueva_salida = Validaciones.ingresar_hora("Ingresar la hora de salida: ")
                entrada_seleccionada.hora_salida = nueva_salida
                entrada_seleccionada.habitacion.estado = "disponible"
                cliente.entrada_activa = False
            case 4:
                nuevo_pago = Validaciones.ingresar_numero(30,200, "Nuevo pago (S/): ", False)
                entrada_seleccionada.pago = nuevo_pago
            case 5:
                op_metodo = Validaciones.ingresar_numero(1,4, "Método de pago:\n1. Efectivo\n2. Yape\n3. Plin\n4. Tarjeta\nOpcion: ")
                if op_metodo == 1: metodo = "efectivo"
                if op_metodo == 2: metodo = "yape"
                if op_metodo == 3: metodo = "plin"
                if op_metodo == 4: metodo = "tarjeta"
                entrada_seleccionada.metodo = metodo
        self.repo.guardar(self.lista_entradas)

        print("Información actualizada con éxito!")
        """