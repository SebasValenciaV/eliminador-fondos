import flet as ft
import webbrowser

SEARCH_ENGINES = {
    "Unsplash": "https://unsplash.com/s/photos/",
    "Pexels": "https://www.pexels.com/search/",
    "Pixabay": "https://pixabay.com/images/search/"
}

def crear_buscador(page):
    query = ft.TextField(label="Buscar imágenes", expand=1)
    
    search_engine = ft.Dropdown(
        label="Selecciona un motor de búsqueda",
        options=[ft.dropdown.Option(name) for name in SEARCH_ENGINES.keys()],
        value="Unsplash",
        expand=1,
    )

    def on_search_click(e):
        term = query.value
        engine = search_engine.value
        if term and engine:
            link = f"{SEARCH_ENGINES[engine]}{term}"
            webbrowser.open(link)

    buscador_content = ft.Container(
        content=ft.Column(
            [
                ft.Text("Buscador de Imágenes Gratuitas", size=20, weight=ft.FontWeight.BOLD),
                ft.Row([query, search_engine], spacing=10),
                ft.ElevatedButton("Buscar", on_click=on_search_click),
            ],
            alignment=ft.MainAxisAlignment.CENTER,
            horizontal_alignment=ft.CrossAxisAlignment.CENTER,
            spacing=20,
        ),
        padding=20,
        width=600,  # Aumentar el ancho del contenedor
        height=200  # Reducir la altura del contenedor
    )

    buscador_dialog = ft.AlertDialog(
        modal=True,
        content=buscador_content,
        actions=[ft.TextButton("Cerrar", on_click=lambda e: page.close(buscador_dialog))]
    )

    page.dialog = buscador_dialog
    buscador_dialog.open = True
    page.update()
