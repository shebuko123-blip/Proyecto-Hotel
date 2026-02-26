from config import Validaciones, RepositorioCliente, RepositorioEntradas, RepositorioHabitaciones, RepositorioInventario, RepositorioVentasCantina, GestorClientes, GestorEntradas, GestorHabitaciones, GestorInventario, RegistroCantina
import msvcrt
import time
from colorama import Fore, Style, Back

RUTAS = {
    "clientes": "Hojas excel/clientes.xlsx",
    "egresos": "Hojas excel/egresos.xlsx",
    "habitaciones": "Hojas excel/habitaciones.xlsx",
    "inventario": "Hojas excel/inventario.xlsx",
    "cantina": "Hojas excel/registrocantina.xlsx",
    "entradas": "Hojas excel/entradas.xlsx"
}

class Programa:

    @staticmethod
    def menu_animado(msj, opciones, seleccion, borrar=False, delay=0):
        if borrar:
            Validaciones.limpiar_consola()
        print(msj)
        for i in range (len(opciones)):
            if i == seleccion:
                if opciones[i] == "Salir" or opciones[i] == "Volver atrás":
                    print(f"{Fore.RED}> {opciones[i]}{Style.RESET_ALL}")
                else:
                    print(f"{Fore.LIGHTBLUE_EX}> {opciones[i]}{Style.RESET_ALL}")
            else:
                print(f"{opciones[i]}")
            time.sleep(delay)    
        print()

    @staticmethod
    def gestion_clientes(g_clientes):
        menu_clientes = [
                        "Registrar nuevo cliente",
                        "Mostrar lista de clientes",
                        "Buscar cliente por DNI",
                        "Mostrar ranking",
                        "Volver atrás"
                    ]
        op_c = 0
        Programa.menu_animado("[=== Menú Clientes ===]", menu_clientes, op_c, True, 0.1)
        while True:
            tecla_c = msvcrt.getch()
            if tecla_c in [b'\x00', b'\xe0']:
                flecha_c = msvcrt.getch()
                if flecha_c == b'H':
                    op_c-=1
                    if op_c < 0: op_c = len(menu_clientes)-1
                elif flecha_c == b'P':
                    op_c+=1
                    if op_c >= len(menu_clientes): op_c = 0
                Programa.menu_animado("[=== Menú Clientes ===]", menu_clientes, op_c, True)
            elif tecla_c == b'\r':
                Validaciones.mostrar_cursor()
                if op_c == 4: break
                elif op_c == 0: g_clientes.registrar_cliente()
                elif op_c == 1: g_clientes.mostrar_lista()
                elif op_c == 2: g_clientes.buscar()
                elif op_c == 3: g_clientes.ver_ranking()
                input("Presione enter para continuar...")
                Programa.menu_animado("[=== Menú Clientes ===]", menu_clientes, op_c, True, 0.1)

    @staticmethod
    def gestion_habitaciones(g_habitaciones:GestorHabitaciones):
        menu_hab = [
            "Registrar nueva habitación",
            "Mostrar lista habitaciones",
            "Buscar habitación",
            "Ver ranking",
            "Volver atrás"
        ]
        op = 0
        Programa.menu_animado("[=== Menú Habitaciones ===]", menu_hab, op, True, 0.1)
        while True:
            tecla = msvcrt.getch()
            if tecla in [b'\x00', b'\xe0']:
                flecha = msvcrt.getch()
                if flecha == b'H': op = (op-1) % len(menu_hab)
                elif flecha == b'P': op = (op+1) % len(menu_hab)
                Programa.menu_animado("[=== Menú Habitaciones ===]", menu_hab, op, True)
            elif tecla == b'\r':
                Validaciones.mostrar_cursor()
                if op == 4: break
                elif op == 0: g_habitaciones.registrar_habitacion()
                elif op == 1: g_habitaciones.mostrar_lista()
                elif op == 2: g_habitaciones.buscar_habitacion()
                elif op == 3: pass
                input("Presiona enter para continuar...")
                Programa.menu_animado("[=== Menú Habitaciones ===]", menu_hab, op, True, 0.1)

    @staticmethod
    def gestion_entradas(g_entradas:GestorEntradas):
        menu_entradas = [
            "Registrar nueva entrada",
            "Mostrar lista entradas",
            "Buscar entrada",
            "Modificar hora",
            "Volver atrás"
        ]
        op = 0
        Programa.menu_animado("[=== Menú Habitaciones ===]", menu_entradas, op, True, 0.1)
        while True:
            tecla = msvcrt.getch()
            if tecla in [b'\x00', b'\xe0']:
                flecha = msvcrt.getch()
                if flecha == b'H': op = (op-1) % len(menu_entradas)
                elif flecha == b'P': op = (op+1) % len(menu_entradas)
                Programa.menu_animado("[=== Menú Habitaciones ===]", menu_entradas, op, True)
            elif tecla == b'\r':
                Validaciones.mostrar_cursor()
                if op == 4: break
                elif op == 0: g_entradas.registrar_entrada()
                elif op == 1: g_entradas.mostrar_lista()
                elif op == 2: g_entradas.modificar_info()
                elif op == 3: pass
                input("Presiona enter para continuar...")
                Programa.menu_animado("[=== Menú Habitaciones ===]", menu_entradas, op, True, 0.1)

    @staticmethod
    def gestion_inventario(g_inventario:GestorInventario, g_cantina:RegistroCantina):
        menu = [
            "Ver lista de productos",
            "Registrar nuevo producto",
            "Buscar producto por código",
            "Registrar venta cantina",
            "Ver lista de ventas",
            "Volver atrás",
        ]
        op = 0
        Programa.menu_animado("[=== Menú Inventario ===]", menu, op, True, 0.1)
        while True:
            tecla = msvcrt.getch()
            if tecla in [b'\x00', b'\xe0']:
                flecha = msvcrt.getch()
                if flecha == b'H': op = (op-1) % len(menu)
                if flecha == b'P': op = (op+1) % len(menu)
                Programa.menu_animado("[=== Menú Inventario ===]", menu, op, True)
            elif tecla == b'\r':
                Validaciones.mostrar_cursor()
                if op == 5: break
                if op == 0: g_inventario.mostrar_lista()
                if op == 1: g_inventario.registrar_producto()
                if op == 2: g_inventario.buscar()
                if op == 3: g_cantina.registrar_venta()
                if op == 4: g_cantina.mostrar_lista()
                input("Presiona Enter para continuar...")
                Programa.menu_animado("[=== Menú Inventario ===]", menu, op, True, 0.1)


    @staticmethod
    def main():
        Validaciones.ocultar_cursor()
        repo_e = RepositorioEntradas(RUTAS["entradas"])
        repo_c = RepositorioCliente(RUTAS["clientes"])
        repo_h = RepositorioHabitaciones(RUTAS["habitaciones"])
        repo_i = RepositorioInventario(RUTAS["inventario"])
        repo_v = RepositorioVentasCantina(RUTAS["cantina"])

        lista_clientes = repo_c.cargar()
        lista_habitaciones = repo_h.cargar()
        lista_productos = repo_i.cargar()

        g_clientes = GestorClientes(repo_c, lista_clientes)
        g_habitaciones = GestorHabitaciones(repo_h, lista_habitaciones)
        g_entradas = GestorEntradas(repo_e, repo_c, repo_h, lista_clientes, lista_habitaciones)
        g_inventario = GestorInventario(repo_i, lista_productos)
        g_cantina = RegistroCantina(repo_v, repo_i, repo_c, lista_productos, lista_clientes)
        
        opciones = [
            "Gestión de clientes",
            "Gestión de habitaciones",
            "Gestión de entradas",
            "Gestión de inventario",
            "Gestión de ingresos y egresos",
            "Salir"
        ]
        seleccion = 0

        ejecutando = True
        
        Programa.menu_animado("[=== Menu Principal ===]",opciones, seleccion, True, 0.1)
        while ejecutando:
            
            #Programa.menu()
            #op = Validaciones.ingresar_numero(1,5, "Opcion: ")
            tecla = msvcrt.getch()
            if tecla in [b'\x00', b'\xe0']:
                flecha = msvcrt.getch()
                if flecha == b'H':
                    seleccion-=1
                    if seleccion < 0: seleccion = len(opciones)-1
                elif flecha == b'P':
                    seleccion+=1
                    if seleccion >= len(opciones): seleccion = 0
                Programa.menu_animado("[=== Menu Principal ===]", opciones, seleccion, True)

            elif tecla == b'\r':
                Validaciones.limpiar_consola()
                if seleccion == 4:
                    print("Programa finalizado...")
                    ejecutando = False
                if seleccion == 0:
                    Programa.gestion_clientes(g_clientes)
                if seleccion == 1:
                    Programa.gestion_habitaciones(g_habitaciones)
                if seleccion == 2:
                    Programa.gestion_entradas(g_entradas)
                if seleccion == 3:
                    Programa.gestion_inventario(g_inventario, g_cantina)
                if ejecutando:
                    Programa.menu_animado("[=== Menú Principal ===]", opciones, seleccion, True, 0.1)
                

Programa.main()
        