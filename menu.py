# menu.py

import flet as ft
from buscador import crear_buscador  # Importar la función para abrir el buscador

class Menu:
    def __init__(self, page):
        self.page = page
        self.create_menu()
        self.setup_close_confirmation()  # Manejar el cierre de la ventana principal

    def create_menu(self):
        # Crear un botón de menú en la app bar
        menu = ft.PopupMenuButton(
            items=[
                ft.PopupMenuItem(text="Cómo funciona", on_click=self.open_help_window),
                ft.PopupMenuItem(text="Buscador de Imágenes", on_click=self.open_image_search),  # Nueva opción de menú
                ft.PopupMenuItem(text="Cerrar aplicación", on_click=self.confirm_exit),
            ]
        )
        
        # Asignar el appbar con el menú
        self.page.appbar = ft.AppBar(
            title=ft.Text("Elimina el fondo de imágenes"),
            center_title=True,
            bgcolor="purple",
            actions=[menu]
        )

    def open_image_search(self, e):
        # Llamar a la función para abrir la ventana de búsqueda
        crear_buscador(self.page)
        
    def confirm_exit(self, e=None):
        # Diálogo para confirmar la salida de la aplicación
        close_dialog = ft.AlertDialog(
            modal=True,
            title=ft.Text("¿Estás seguro de que quieres salir?"),
            content=ft.Text("Cualquier progreso no guardado se perderá."),
            actions=[
                ft.TextButton("Sí", on_click=lambda e: self.page.window.destroy()),  # Cerrar la aplicación
                ft.TextButton("No", on_click=lambda e: self.page.close(close_dialog))  # Cerrar el diálogo
            ],
            actions_alignment=ft.MainAxisAlignment.END,
        )
        self.page.overlay.append(close_dialog)  # Añadir el diálogo a la página
        close_dialog.open = True  # Abrir el diálogo
        self.page.update()

    def open_help_window(self, e):
        # Crear un AlertDialog para explicar el funcionamiento con tamaño controlado
        help_dialog = ft.AlertDialog(
            modal=True,
            title=ft.Text("Cómo funciona el programa", color=ft.colors.WHITE),
            content=ft.Container(
                content=ft.Column(
                    [
                        ft.Text(
                            "Este programa elimina el fondo de imágenes.",
                            weight=ft.FontWeight.BOLD,
                            color=ft.colors.RED
                        ),
                        ft.Text("0. Selecciona la opción buscar imágenes gratuítas en el menú, y descargalas a tu equipo.",
                                color=ft.colors.WHITE),
                        ft.Text("1. Presiona 'Procesar carpeta de imágenes' o 'Cargar imagen con fondo'.",
                                color=ft.colors.WHITE),
                        ft.Text("2. Selecciona la carpeta donde se guardarán las imágenes sin fondo.",
                                color=ft.colors.WHITE),
                        ft.Text("3. El proceso tardará más o menos en función de la cantidad de imágenes a procesar.",
                                color=ft.colors.WHITE),
                        ft.Text("4. Las imágenes sin fondo se guardarán en la carpeta seleccionada. Todas ellas tendrán el mismo nombre \npero se añadirá '_sinfondo.png' al final.",
                                color=ft.colors.WHITE),
                    ],
                    alignment=ft.MainAxisAlignment.CENTER,
                    horizontal_alignment=ft.CrossAxisAlignment.CENTER,
                    spacing=10
                ),
                padding=ft.padding.all(10),  # Padding interno
                width=400,  # Ancho fijo para el diálogo
                height=250,  # Altura controlada
                alignment=ft.alignment.center  # Centrar contenido dentro del contenedor
            ),
            actions=[
                ft.TextButton("Cerrar", on_click=lambda e: self.page.close(help_dialog))
            ],
            actions_alignment=ft.MainAxisAlignment.END,
            bgcolor=ft.colors.BLACK,
            inset_padding=ft.Padding(20, 20, 20, 20),  # Padding externo ajustado
        )
        self.page.overlay.append(help_dialog)
        help_dialog.open = True  # Abrir el diálogo de ayuda
        self.page.update()

    def setup_close_confirmation(self):
        # Manejar el evento de cierre de la ventana (cuando se pulsa la X)
        def handle_window_event(e):
            if e.data == "close":
                self.confirm_exit()  # Abrir el diálogo de confirmación de salida

        self.page.window.prevent_close = True  # Evitar el cierre directo de la ventana
        self.page.window.on_event = handle_window_event  # Asignar el evento de cierre
