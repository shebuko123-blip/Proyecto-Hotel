import time
from validaciones import *
import msvcrt
def menu_animado(msj, lista_opciones, seleccion, delay=0):
    print(f"[=== {msj} ===]")
    for i, opcion in enumerate(lista_opciones):
        if i == seleccion:
            print(f"> {opcion} <")
        else:
            print(f"  {opcion}  ")
        time.sleep(delay)

def cambiar_opcion(msj, lista_opciones, seleccion, delay=0):
    print(f"[=== {msj} ===]")
    for i, opcion in enumerate(lista_opciones):
        if i == seleccion:
            print(f"> {opcion} <")
        else:
            print(f"  {opcion}  ")
        time.sleep(delay)


def main():
    Validaciones.ocultar_cursor()
    lista_opciones = {
        "Registrar Cliente",
        "Mostrar lista", 
        "Buscar",
        "Salir"
    }
    seleccion = 0
    ejecutando = True
    Validaciones.limpiar_consola()
    menu_animado("Menú Principal", lista_opciones, seleccion, 0.1)
    while ejecutando:
        tecla = msvcrt.getch()
        if tecla in [b'\x00', b'\xe0']: #Alguna flecha
            flecha = msvcrt.getch()
            if flecha == b'H': seleccion = (seleccion-1)%len(lista_opciones)
            if flecha == b'P': seleccion = (seleccion+1)%len(lista_opciones)
            Validaciones.limpiar_consola()
            cambiar_opcion("Menú Principal", lista_opciones, seleccion)
        elif tecla == b'\r': #Enter
            pass

main()