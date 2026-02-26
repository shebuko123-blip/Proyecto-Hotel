import os
import sys
import datetime as dt

class Validaciones:
    @staticmethod
    def ingresar_numero(min, max, msj, entero=True):
        while True:
            try:
                num = int(input(msj)) if entero else float(input(msj))
                if num < min or num > max:
                    print(f"El número ingresado está fuera del rango: [{min}-{max}]. Intentar nuevamente.")
                else:
                    return num
            except ValueError:
                tipo = "entero" if entero else "numérico"
                print(f"Error. Debe ingresar un valor {tipo}!")
    @staticmethod
    def ingresar_cadena(min, max, msj, tipo=1):
        while True:
            cadena = input(msj).lower().strip()
            if len(cadena) < min or len(cadena) > max:
                print(f"Cadena fuera del límite de caracteres: [{min}-{max}]. Intentar nuevamente.")
                continue
            if tipo == 1:
                if cadena.replace(" ","").isalpha():
                    return cadena
                else:
                    print(f"La cadena debe contener solo letras.")
                    continue
            elif tipo == 2:
                if cadena.isnumeric():
                    return cadena
                else:
                    print(F"La cadena debe contener solo números.")
                    continue
            elif tipo == 3:
                if cadena.replace(" ","").isalnum():
                    return cadena
                else:
                    print(f"La cadena debe contener letras y numeros.")
                    continue
            else:
                print(f"Parámetro numérico erróneo.")
    
    @staticmethod
    def ingresar_correo(msj):
        while True:
            correo = input(msj).lower().strip()
            if 7 < len(correo) > 254:
                print("Error. El correo no puede ser menor de 7 ni mayor de 254 caracteres!")
                continue
            if correo.count("@") != 1:
                print("El correo debe contener exactamente una arroba (@).")
                continue
            prohibidos = "( )[],!#&%/=?"
            if any(c in prohibidos for c in correo):
                print("El correo contiene caracteres prohibidos.")
                continue

            dominiosValidos = ["gmail.com", "hotmail.com", "yahoo.com", "outlook.com"]
            parteLocal, dominio = correo.split("@")
            if dominio not in dominiosValidos:
                print("El dominio ingresado es inválido!")
                continue
            return correo
        
    @staticmethod
    def ingresar_hora(msj):
        print(msj)
        hora = Validaciones.ingresar_numero(1,23, "Horas: ")
        minutos = Validaciones.ingresar_numero(1,59, "Minutos: ")
        return str(hora) + ":" + str(minutos)
    
    @staticmethod
    def elegir_categoria():
        print("[=== Selección del producto a vender ===]")
        print("Categoría:")
        print("1. Snacks")
        print("2. Aseo personal")
        print("3. Licores")
        print("4. Gaseosas")
        print("5. Energizantes")
        print("6. Preservativos")
        op = Validaciones.ingresar_numero(1,6, "Opción: ")
        match op:
            case 1: cat = "snacks"
            case 2: cat = "aseo"
            case 3: cat = "licores"
            case 4: cat = "gaseosas"
            case 5: cat = "energizantes"
            case 6: cat = "preservativos"
        return cat

    @staticmethod
    def ingresar_fecha(msj):
        while True:
            fecha_ingresada = input(msj)
            try:
                fecha = dt.strptime(fecha_ingresada, "%d/%m/%Y")
                hoy = dt.datetime.today()
                if fecha > hoy:
                    print("Fecha incorrecta.")
                return fecha.strftime("%d/%m/%Y")
            except ValueError:
                print("Formato incorrecto!")

    @staticmethod
    def limpiar_consola():
        os.system("cls") if os.name == "nt" else os.system("clear")

    @staticmethod
    def ocultar_cursor():
        sys.stdout.write("\033[?25l")
        sys.stdout.flush()

    @staticmethod
    def mostrar_cursor():
        sys.stdout.write("\033[?25h")
        sys.stdout.flush()
            


