import flet as ft
from rembg import remove
from PIL import Image
import os
import io

# Función para eliminar el fondo de una imagen
def eliminar_fondo(input_image_path, output_image_path):
    try:
        with open(input_image_path, "rb") as input_file:
            input_data = input_file.read()

        output_data = remove(input_data)

        img = Image.open(io.BytesIO(output_data)).convert("RGBA")
        img.save(output_image_path, format="PNG")
        print(f"Imagen sin fondo guardada en {output_image_path}")
    except Exception as e:
        print(f"Error al eliminar el fondo: {e}")

def main(page: ft.Page):
    page.title = "Quitar fondo de imágenes"
    page.window.width = 800
    page.window.height = 600
   # page.window.resizable = False  # Bloquear redimensionamiento
    page.horizontal_alignment = ft.CrossAxisAlignment.CENTER
    page.vertical_alignment = ft.MainAxisAlignment.CENTER

    default_image_path = "assets/default-image.png"

    img_input = ft.Text(value="No hay imagen seleccionada", expand=1)
    original_image_preview = ft.Image(src=default_image_path, width=150, height=150, fit=ft.ImageFit.CONTAIN)
    removed_bg_image_preview = ft.Image(src=default_image_path, width=150, height=150, fit=ft.ImageFit.CONTAIN)
    output_name_field = ft.TextField(label="Nombre de la imagen sin fondo (añade .png al final)", width=250)
    output_dir = ""

    def on_file_chosen(e: ft.FilePickerResultEvent):
        if e.files:
            img_input.value = e.files[0].path
            if os.path.exists(e.files[0].path):
                original_image_preview.src = e.files[0].path
            else:
                original_image_preview.src = default_image_path
            removed_bg_image_preview.src = default_image_path
            page.update()

    def on_folder_chosen(e: ft.FilePickerResultEvent):
        nonlocal output_dir
        if e.path:
            output_dir = e.path
            output_path = os.path.join(output_dir, output_name_field.value)
            eliminar_fondo(img_input.value, output_path)
            if os.path.exists(output_path):
                removed_bg_image_preview.src = output_path
            else:
                removed_bg_image_preview.src = default_image_path
            page.update()
            snack_bar = ft.SnackBar(ft.Text(f"Imagen guardada en {output_path}"))
            page.overlay.append(snack_bar)
            snack_bar.open = True
            page.update()

    file_picker = ft.FilePicker(on_result=on_file_chosen)
    page.overlay.append(file_picker)

    def cargar_imagen(e):
        file_picker.pick_files()

    def guardar_imagen(e):
        if not img_input.value or not output_name_field.value:
            snack_bar = ft.SnackBar(ft.Text("Por favor, selecciona una imagen y especifica un nombre."))
            page.overlay.append(snack_bar)
            snack_bar.open = True
            page.update()
            return
        file_picker.on_result = on_folder_chosen
        file_picker.get_directory_path()

    # Ajustar igual distancia en ambas columnas
    container_padding = ft.Padding(top=30, left=10, right=10, bottom=10)

    page.add(
        ft.Row(
            [
                ft.Container(
                    content=ft.Column(
                        [
                            ft.Text("Selecciona una imagen para quitar el fondo:", weight=ft.FontWeight.BOLD),
                            original_image_preview,
                            ft.Row([img_input, ft.ElevatedButton("Cargar imagen con fondo", on_click=cargar_imagen)]),
                        ],
                        alignment=ft.MainAxisAlignment.START,
                      
                        horizontal_alignment=ft.CrossAxisAlignment.CENTER,
                    ),
                    padding=container_padding,
                ),
                ft.Container(
                    content=ft.Column(
                        [
                            ft.Text("Vista previa de la imagen sin fondo:", weight=ft.FontWeight.BOLD),
                            removed_bg_image_preview,
                            output_name_field,
                            ft.ElevatedButton("Guardar imagen sin fondo", on_click=guardar_imagen),
                        ],
                        alignment=ft.MainAxisAlignment.START,
                        horizontal_alignment=ft.CrossAxisAlignment.CENTER,
                    ),
                    padding=container_padding,
                ),
            ],
            alignment=ft.MainAxisAlignment.SPACE_AROUND,
            spacing=40,
        )
    )

# Ejecutar la aplicación de Flet
ft.app(target=main)
