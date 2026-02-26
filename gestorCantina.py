from config import pd, Validaciones, VentaCantina

class RepositorioVentasCantina:
    def __init__(self, ruta):
        self.ruta = ruta

    def cargar(self, lista_productos, lista_clientes):
        df = pd.read_excel(self.ruta, dtype={"CODIGO": str, "DNI_CLIENTE":str})
        lista = []
        for _, fila in df.iterrows():
            cod_en_fila = fila["CODIGO"]
            dni_en_fila = fila["DNI_CLIENTE"]

            producto = next((p for p in lista_productos if p.codigo == cod_en_fila), None)
            cliente = next((c for c in lista_clientes if c.dni == dni_en_fila), None)
        
            if producto is None or cliente is None:
                print("No se ha encontrado el producto o cliente.")
                continue
            nueva = VentaCantina(producto, cliente, fila["CANTIDAD"], fila["FECHA"])
            lista.append(nueva)
        return lista
    
    def guardar(self, registro_ventas):
        data = []
        for v in registro_ventas:
            data.append(v.to_dict())
        df = pd.DataFrame(data)
        df.to_excel(self.ruta, index=False)

class RegistroCantina:
    def __init__(self, repositorio, repo_prod, repo_cli, lista_productos, lista_clientes):
        self.repo = repositorio
        self.repo_prod = repo_prod
        self.repo_cli = repo_cli
        self.lista_productos = lista_productos
        self.lista_clientes = lista_clientes
        datos_cargados = self.repo.cargar(lista_productos, lista_clientes)
        self.registro = datos_cargados if datos_cargados is not None else []

    def retorna_codigo_producto(self):
        cat = Validaciones.elegir_categoria() #Elegir una categoría

        print(f"Productos disponibles para la categoría de {cat.capitalize()}: ")
        lista = [p for p in self.lista_productos if p.categoria == cat and p.stock > 0]
        if not lista:
            return
        for i, p in enumerate(lista, start = 1):
            print(f"{i}. {p.nombre}")
        
        op_prod = Validaciones.ingresar_numero(1, len(lista), "Prroducto N°: ")-1
        return lista[op_prod].codigo

    def registrar_venta(self):
        cod_producto = self.retorna_codigo_producto()
        if not cod_producto:
            print("Sin coincidencias...")
            return

        dni_cliente = Validaciones.ingresar_cadena(8,8, "DNI del cliente: ",2)
        cliente = next((c for c in self.lista_clientes if c.dni == dni_cliente), None)
        producto = next((p for p in self.lista_productos if p.codigo == cod_producto), None)  
        if cliente is None:
            print(f"El DNI '{dni_cliente}' no se encuentra registrado en la base de datos.")
            return
        
        print(f"\nProducto seleccionado: {producto.nombre.title()} | Precio S/: {producto.precio} | Stock: {producto.stock} unidades")
        cantidad = Validaciones.ingresar_numero(1, producto.stock, f"Cantidad a consumir: ")

        ahora = pd.Timestamp.now() #Capturar el momento exacto donde se realiza la venta 
        if ahora.hour < 8:
            fecha = (ahora-pd.Timedelta(days=1)).strftime("%d-%m-%Y")
        else:
            fecha = ahora.strftime("%d-%m-%Y")

        nueva_venta = VentaCantina(producto, cliente, cantidad, fecha)
        cliente.c_cantina+= producto.precio * cantidad
        producto.stock -= cantidad
        producto.total_vendido += cantidad
        producto.total_generado += cantidad * producto.precio
        self.registro.append(nueva_venta)

        self.repo_cli.guardar(self.lista_clientes)
        self.repo_prod.guardar(self.lista_productos)
        self.repo.guardar(self.registro)

        print("\nVenta registrada exitosamente.")

    def mostrar_lista(self):
        if not self.registro:
            print("No hay ventas para mostrar.")
            return
        print(f"{'N°':<5}{'PRODUCTO':<20}{'CODIGO':<10}{'CLIENTE':<35}{"DNI":<15}{'CANTIDAD':<12}{'PAGO S/.':<12}{'FECHA':<15}")
        print("-"*120)
        for i, v in enumerate(self.registro, start=1):
            print(f"{i}.   {v}")