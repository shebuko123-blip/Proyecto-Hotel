from validaciones import *

class Persona:
    def __init__(self, nombres, aPaterno, aMaterno, dni, edad, sexo, celular, correo):
        self.nombres = nombres
        self.aPaterno = aPaterno
        self.aMaterno = aMaterno
        self.dni = dni
        self.edad = edad
        self.sexo = sexo
        self.celular = celular
        self.correo = correo

class Cliente(Persona):
    def __init__(self, nombres, aPaterno, aMaterno, dni, edad, sexo, celular, correo, entradas=0, c_entradas=0, c_cantina=0):
        super().__init__(nombres, aPaterno, aMaterno, dni, edad, sexo, celular, correo)
        self.entradas = entradas
        self.c_entradas = c_entradas
        self.c_cantina = c_cantina
        self.historial_hab = {}
        self.entrada_activa = False

    @property
    def consumo_total(self):
        return self.c_entradas + self.c_cantina 
    @property
    def hab_favorita(self):
        if not self.historial_hab:
            return None
        return max(self.historial_hab, key = lambda hab: self.historial_hab[hab][0])
    
    def info_hab_especifica(self, nro_hab):
        if nro_hab in self.historial_hab:
            visitas = self.historial_hab[nro_hab][0]
            dinero = self.historial_hab[nro_hab][1]
            print(f"En la habitación {nro_hab}:")
            print(f"- Ha estado {visitas} veces.")
            print(f"- Ha consumido un total de S/.{dinero}")
        else:
            print("El cliente nunca se ha hospedado en esa habitación.")

    def to_dict(self):
        return {
            "NOMBRES": self.nombres,
            "A. PATERNO": self.aPaterno,
            "A. MATERNO": self.aMaterno,
            "DNI": self.dni,
            "EDAD": self.edad,
            "SEXO": self.sexo,
            "CELULAR": self.celular,
            "CORREO": self.correo,
            "ENTRADAS": self.entradas,
            "C. ENTRADAS": self.c_entradas,
            "C. CANTINA": self.c_cantina,
            "C. TOTAL": self.consumo_total
        }
    
    def info(self):
        print("\n[=== Información general del cliente ===]")
        print(f"Nombre completo: {self.nombres.title()} {self.aPaterno.capitalize()} {self.aMaterno.capitalize()}")
        print(f"DNI: {self.dni}")
        print(f"Edad: {self.edad}")
        sexo = "Masculino" if self.sexo == "M" else "Femenino"
        print(f"Sexo: {sexo}")
        print(f"Celular: {self.celular}")
        print(f"Correo: {self.correo}")
        print(f"Entradas: {self.entradas}")
        print(f"Consumo de entradas: S/{self.c_entradas}")
        print(f"Consumo de cantina: S/{self.c_cantina}")
        print(f"Total consumido: S/{self.consumo_total}")

    def __str__(self):
        nombre_completo = (f"{self.nombres} {self.aPaterno} {self.aMaterno}").title()
        return f"{nombre_completo:<35}{self.dni:<15}{self.edad:<10}{self.sexo:<10}{self.celular:<15}{self.correo:<35}{self.entradas:<12}{self.c_entradas:<15}{self.c_cantina:<15}{self.consumo_total:<15}"
    

    