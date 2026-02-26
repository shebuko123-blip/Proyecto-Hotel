from config import pd, Validaciones, Producto

class RepositorioInventario:
    def __init__(self, ruta):
        self.ruta = ruta

    def cargar(self):
        df = pd.read_excel(self.ruta)
        lista = []
        for _, fila in df.iterrows():
            nuevo = Producto(fila["CODIGO"], fila["NOMBRE"], fila["CATEGORIA"], fila["PRECIO"], 
                             fila["STOCK"], fila["VENDIDO"], fila["GENERADO"])
            lista.append(nuevo)
        return lista
    
    def guardar(self, inventario):
        data = []
        for i in inventario:
            data.append(i.to_dict())
        df = pd.DataFrame(data)
        df.to_excel(self.ruta, index=False)
    

class GestorInventario:
    def __init__(self, repositorio, lista_productos):
        self.repo = repositorio
        self.inventario = lista_productos

    def generar_codigo(self, categoria_seleccionada):
        prefijos = {
            "snacks": "SNK",
            "licores": "LIC",
            "aseo": "ASE",
            "gaseosas": "GAS",
            "energizantes": "NRG",
            "preservativos": "PRE"
        }
        prefijo = prefijos.get(categoria_seleccionada, "GEN")
        contador = sum(1 for p in self.inventario if p.categoria == categoria_seleccionada) + 1
        return f"{prefijo}-{contador:03d}"

    def registrar_producto(self):
        cat = Validaciones.elegir_categoria()
        codigo = self.generar_codigo(cat)
        nombre = Validaciones.ingresar_cadena(3,30, "Nombre del producto: ")
        precio = Validaciones.ingresar_numero(1,100, "Precio (S/): ", False)
        stock = Validaciones.ingresar_numero(1,100, "Stock disponible: ")
        nuevo_producto = Producto(codigo, nombre, cat, precio, stock)
        self.inventario.append(nuevo_producto)
        self.repo.guardar(self.inventario)

        print(f"Producto registrado con éxito con el código '{codigo}'.")

    def buscar(self):
        cod_producto = Validaciones.ingresar_cadena(7,7, "Ingrese el código del producto a registrar: ")
        producto = None
        while producto is None:
            producto = next((p for p in self.lista_productos if p.codigo == cod_producto), None)
            if producto is None:
                print("Código incorrecto. Inténtelo nuevamente.")
        
        print("\n[=== Información del producto ===]")
        print(f"- Código: {producto.codigo}")
        print(f"- Nombre: {producto.nombre}")
        print(f"- Precio: {producto.precio}")
        print(f"- Stock: {producto.stock}")
        print(f"- Total vendido: {producto.total_vendido} unidades.")
        print(f"- Total generado: S/{producto.total_generado}")

    def mostrar_lista(self):
        if not self.inventario:
            print("No hay productos para mostrar.")
            return
        
        print(f"{'N°':<5}{'CODIGO':<10}{'NOMBRE':<20}{'CATEGORIA':<15}{'PRECIO S/.':<12}{'STOCK':<10}{'U. VENDIDAS':<15}{"INGRESO S/.":<12}")
        print("-"*100)
        for i, p in enumerate(self.inventario, start=1):
            print(f"{i}.   {p}")