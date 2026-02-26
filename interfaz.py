from rich.console import Console
from rich.table import Table
from rich.panel import Panel
from rich.text import Text
from rich import box
import os

console = Console()

class Interfaz:
    
    @staticmethod
    def limpiar():
        os.system('cls' if os.name == 'nt' else 'clear')

    @staticmethod
    def titulo(texto):
        Interfaz.limpiar()
        console.print(Panel.fit(
            f"[bold cyan]{texto.upper()}[/bold cyan]", 
            box=box.DOUBLE, 
            padding=(0, 4),
            border_style="cyan"
        ), justify="center")

    @staticmethod
    def mensaje_exito(mensaje):
        console.print(f"\n[bold green]✅ ÉXITO:[/bold green] {mensaje}")

    @staticmethod
    def mensaje_error(mensaje):
        console.print(f"\n[bold red]❌ ERROR:[/bold red] {mensaje}")
        
    @staticmethod
    def mensaje_info(mensaje):
        console.print(f"\n[bold yellow]ℹ️ INFO:[/bold yellow] {mensaje}")

    @staticmethod
    def mostrar_tabla(titulo, columnas, filas):
        """
        columnas: lista de strings ["DNI", "Nombre", ...]
        filas: lista de listas [["123", "Juan"], ["456", "Ana"]]
        """
        table = Table(title=titulo, box=box.ROUNDED, header_style="bold magenta")

        for col in columnas:
            table.add_column(col, justify="center")

        for fila in filas:
            # Convertimos todo a string para evitar errores de renderizado
            fila_str = [str(item) for item in fila]
            table.add_row(*fila_str)

        console.print(table, justify="center")

    @staticmethod
    def mostrar_ficha(titulo, datos_dict):
        """Muestra datos de un solo objeto en un panel bonito"""
        texto_cuerpo = ""
        for clave, valor in datos_dict.items():
            texto_cuerpo += f"[bold cyan]{clave}:[/bold cyan] {valor}\n"
        
        console.print(Panel(
            texto_cuerpo, 
            title=f"[bold yellow]{titulo}[/bold yellow]",
            subtitle="Detalle del registro",
            expand=False,
            border_style="blue"
        ))