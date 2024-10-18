import flet as ft
from rembg import remove
from PIL import Image
import os
import io
import subprocess
import platform

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

def eliminar_fondo_carpeta(carpeta_origen, carpeta_destino):
    try:
        for filename in os.listdir(carpeta_origen):
            if filename.lower().endswith(('.png', '.jpg', '.jpeg')):
                input_image_path = os.path.join(carpeta_origen, filename)
                output_image_path = os.path.join(carpeta_destino, filename.replace(".png", "_sinfondo.png").replace(".jpg", "_sinfondo.png").replace(".jpeg", "_sinfondo.png"))
                eliminar_fondo(input_image_path, output_image_path)
        print("Fondo eliminado de todas las imágenes en la carpeta.")
    except Exception as e:
        print(f"Error al procesar la carpeta: {e}")

# Función para abrir la carpeta de destino
def abrir_carpeta_destino(carpeta):
    try:
        if platform.system() == "Windows":
            subprocess.run(["explorer", carpeta])
        elif platform.system() == "Linux":
            subprocess.run(["xdg-open", carpeta])
        else:
            print("Sistema operativo no soportado")
    except Exception as e:
        print(f"Error al abrir la carpeta: {e}")

def main(page: ft.Page):
    page.title = "Quitar fondo de imágenes"
    page.window.width = 800
    page.window.height = 600
    page.horizontal_alignment = ft.CrossAxisAlignment.CENTER
    page.vertical_alignment = ft.MainAxisAlignment.CENTER

    default_image_path = "assets/default-image.png"

    img_input = ft.Text(value="No hay imagen seleccionada", expand=1)
    original_image_preview = ft.Image(src=default_image_path, width=150, height=150, fit=ft.ImageFit.CONTAIN)
    removed_bg_image_preview = ft.Image(src=default_image_path, width=150, height=150, fit=ft.ImageFit.CONTAIN)
    output_dir = ""
    input_image_path = ""

    # Función para manejar la selección de archivo (imagen)
    def on_file_chosen(e: ft.FilePickerResultEvent):
        nonlocal input_image_path
        if e.files:
            input_image_path = e.files[0].path
            img_input.value = input_image_path
            if os.path.exists(input_image_path):
                original_image_preview.src = input_image_path
            else:
                original_image_preview.src = default_image_path
            removed_bg_image_preview.src = default_image_path
            page.update()

    # Función para manejar la selección de carpeta de destino
    def on_folder_chosen(e: ft.FilePickerResultEvent):
        nonlocal output_dir
        if e.path:
            output_dir = e.path
            snack_bar = ft.SnackBar(ft.Text(f"Carpeta de destino seleccionada: {output_dir}"))
            page.overlay.append(snack_bar)
            snack_bar.open = True
            page.update()

            # Si hay una imagen cargada, procesarla
            if input_image_path:
                output_name = os.path.basename(input_image_path).rsplit('.', 1)[0] + "_sinfondo.png"
                output_path = os.path.join(output_dir, output_name)
                eliminar_fondo(input_image_path, output_path)
                if os.path.exists(output_path):
                    removed_bg_image_preview.src = output_path
                    snack_bar = ft.SnackBar(ft.Text(f"Imagen guardada en {output_path}"))
                    page.overlay.append(snack_bar)
                    snack_bar.open = True
                else:
                    removed_bg_image_preview.src = default_image_path
                page.update()

    # Función para manejar la selección de carpeta con imágenes
    def on_folder_with_images_chosen(e: ft.FilePickerResultEvent):
        if e.path:
            carpeta_origen = e.path
            if not output_dir:
                snack_bar = ft.SnackBar(ft.Text("Por favor, selecciona una carpeta de destino antes de procesar las imágenes."))
                page.overlay.append(snack_bar)
                snack_bar.open = True
                page.update()
                return

            eliminar_fondo_carpeta(carpeta_origen, output_dir)
            snack_bar = ft.SnackBar(ft.Text(f"Fondo eliminado de todas las imágenes en {carpeta_origen}"))
            page.overlay.append(snack_bar)
            snack_bar.open = True
            page.update()

    file_picker = ft.FilePicker(on_result=on_file_chosen)
    page.overlay.append(file_picker)

    folder_picker = ft.FilePicker(on_result=on_folder_with_images_chosen)
    page.overlay.append(folder_picker)

    folder_picker_output = ft.FilePicker(on_result=on_folder_chosen)
    page.overlay.append(folder_picker_output)

    # Botón para cargar imagen
    def cargar_imagen(e):
        file_picker.pick_files()

    # Botón para seleccionar carpeta con imágenes
    def seleccionar_carpeta_imagenes(e):
        folder_picker.get_directory_path()

    # Botón para seleccionar carpeta de destino
    def seleccionar_carpeta_destino(e):
        folder_picker_output.get_directory_path()

    # Botón para abrir la carpeta de destino
    def abrir_carpeta_destino_click(e):
        if output_dir:
            abrir_carpeta_destino(output_dir)
        else:
            snack_bar = ft.SnackBar(ft.Text("Primero selecciona una carpeta de destino."))
            page.overlay.append(snack_bar)
            snack_bar.open = True
            page.update()

    # Ajustar igual distancia en ambas columnas
    container_padding = ft.Padding(top=30, left=10, right=10, bottom=10)

    # Componentes de la UI
    page.add(
        ft.Row(
            [
                # Primera columna
                ft.Container(
                    content=ft.Column(
                        [
                            ft.Text("Selecciona una imagen para quitar el fondo:", weight=ft.FontWeight.BOLD),
                            original_image_preview,
                            ft.Row(
                                [
                                    img_input, 
                                    ft.ElevatedButton("Cargar imagen con fondo", on_click=cargar_imagen)
                                ]
                            ),
                            ft.Row(
                                [
                                    ft.ElevatedButton("Procesar carpeta de imágenes", on_click=seleccionar_carpeta_imagenes)
                                ]
                            ),
                        ],
                        alignment=ft.MainAxisAlignment.START,
                        horizontal_alignment=ft.CrossAxisAlignment.CENTER,
                    ),
                    padding=container_padding,
                ),
                # Segunda columna
                ft.Container(
                    content=ft.Column(
                        [
                            ft.Text("Vista previa de la imagen sin fondo:", weight=ft.FontWeight.BOLD),
                            removed_bg_image_preview,
                            ft.ElevatedButton("Seleccionar carpeta destino", on_click=seleccionar_carpeta_destino),
                            ft.ElevatedButton("Abrir carpeta destino", on_click=abrir_carpeta_destino_click),
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
