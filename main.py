import flet as ft
from rembg import remove
from PIL import Image
import pystray
from pystray import MenuItem as Item, Icon
import os
import io
import subprocess
import platform
from menu import Menu  # Importar el menú
import threading

# Obtén el directorio del archivo actual
BASE_DIR = os.path.dirname(os.path.abspath(__file__))

# Función para eliminar el fondo de una imagen
def eliminar_fondo(input_image_path, output_image_path):
    try:
        with open(input_image_path, "rb") as input_file:
            input_data = input_file.read()

        output_data = remove(input_data)

        img = Image.open(io.BytesIO(output_data)).convert("RGBA")
        img.save(output_image_path, format="PNG")
    except Exception as e:
        print(f"Error al eliminar el fondo: {e}")

def eliminar_fondo_carpeta(carpeta_origen, carpeta_destino, progress, progress_text, snack_bar, page):
    try:
        imagenes = [f for f in os.listdir(carpeta_origen) if f.lower().endswith(('.png', '.jpg', '.jpeg'))]
        total = len(imagenes)
        progress.value = 0
        progress.visible = True  # Mostrar la barra de progreso al comenzar
        progress_text.visible = True  # Mostrar el texto "Progreso:" al comenzar
        page.update()

        for index, filename in enumerate(imagenes, start=1):
            input_image_path = os.path.join(carpeta_origen, filename)
            output_image_path = os.path.join(carpeta_destino, filename.replace(".png", "_sinfondo.png").replace(".jpg", "_sinfondo.png").replace(".jpeg", "_sinfondo.png"))
            eliminar_fondo(input_image_path, output_image_path)

            # Actualiza el progreso
            progress.value = index / total
            snack_bar.content.value = f"Procesando {index}/{total}: {filename}"
            snack_bar.open = True
            page.update()

        snack_bar.content.value = f"Fondo eliminado de todas las imágenes en {carpeta_origen}"
        snack_bar.open = True
        progress.visible = False  # Ocultar la barra de progreso al terminar
        progress_text.visible = False  # Ocultar el texto "Progreso:" al terminar
        page.update()
    except Exception as e:
        snack_bar.content.value = f"Error al procesar la carpeta: {e}"
        snack_bar.open = True
        progress.visible = False  # Ocultar la barra de progreso en caso de error
        progress_text.visible = False  # Ocultar el texto "Progreso:" en caso de error
        page.update()

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
        
def create_tray_icon(page):
    def quit_action(icon, item):
        icon.stop()


    image = Image.open(os.path.join(BASE_DIR, "assets/tray-icon.png"))  # icono bandeja del sistema
    icon = pystray.Icon("URL Shortener", image, menu=pystray.Menu(
        Item('Mostrar ventana', lambda: None),  
        Item('Salir', lambda icon, item: quit_action(icon, item))
    ))
    
    def run_tray():
        icon.run()

    tray_thread = threading.Thread(target=run_tray, daemon=True)
    tray_thread.start()

async def main(page: ft.Page):
    page.title = "Quitar fondo de imágenes"
    page.theme_mode = "dark"
    
    # Ajustar el tamaño de la ventana usando la nueva API
    page.window.width = 800
    page.window.height = 600
    page.horizontal_alignment = ft.CrossAxisAlignment.CENTER
    page.vertical_alignment = ft.MainAxisAlignment.CENTER
    
    # Inicializa el menú
    Menu(page)  # Crear el menú en la ventana principal

    default_image_path = "assets/default-image.png"

    img_input = ft.Text(value="No hay imagen seleccionada", expand=1)
    original_image_preview = ft.Image(src=default_image_path, width=150, height=150, fit=ft.ImageFit.CONTAIN)
    removed_bg_image_preview = ft.Image(src=default_image_path, width=150, height=150, fit=ft.ImageFit.CONTAIN)
    output_dir = ""
    input_image_path = ""
    carpeta_origen = ""

    # Añadir barra de progreso y texto de "Progreso", inicialmente invisibles
    progress = ft.ProgressBar(width=400, visible=False)
    progress_text = ft.Text("Progreso:", weight=ft.FontWeight.BOLD, visible=False)

    # SnackBar para mostrar mensajes
    snack_bar = ft.SnackBar(ft.Text(""))

    # Función para restablecer los valores
    def reset_app():
        nonlocal input_image_path, output_dir, carpeta_origen
        input_image_path = ""
       # output_dir = ""
        carpeta_origen = ""
        img_input.value = "No hay imagen seleccionada"
        original_image_preview.src = default_image_path
        removed_bg_image_preview.src = default_image_path
        progress.value = 0
        progress.visible = False  # Ocultar la barra de progreso cuando se reinicie
        progress_text.visible = False  # Ocultar el texto "Progreso" cuando se reinicie
        page.update()

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
            snack_bar.content.value = f"Carpeta de destino seleccionada: {output_dir}"
            snack_bar.open = True
            page.update()

            # Procesar todas las imágenes de la carpeta de origen
            if carpeta_origen:
                eliminar_fondo_carpeta(carpeta_origen, output_dir, progress, progress_text, snack_bar, page)
                reset_app()  # Reiniciar la aplicación después de procesar
            elif input_image_path:  # Procesar una sola imagen si no hay carpeta de origen
                output_name = os.path.basename(input_image_path).rsplit('.', 1)[0] + "_sinfondo.png"
                output_path = os.path.join(output_dir, output_name)
                eliminar_fondo(input_image_path, output_path)
                
                # Asegúrate de que la imagen sin fondo se actualice en la vista previa
                if os.path.exists(output_path):
                    removed_bg_image_preview.src = output_path
                    snack_bar.content.value = f"Imagen guardada en {output_path}"
                    snack_bar.open = True
                else:
                    removed_bg_image_preview.src = default_image_path
                page.update()
                reset_app()  # Reiniciar la aplicación después de procesar

    # Función para manejar la selección de carpeta con imágenes
    def on_folder_with_images_chosen(e: ft.FilePickerResultEvent):
        nonlocal carpeta_origen
        if e.path:
            carpeta_origen = e.path
            if not output_dir:
                snack_bar.content.value = "Por favor, selecciona una carpeta de destino antes de procesar las imágenes."
                snack_bar.open = True
                page.update()
                return

            eliminar_fondo_carpeta(carpeta_origen, output_dir, progress, progress_text, snack_bar, page)
            reset_app()  # Reiniciar la aplicación después de procesar

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
            snack_bar.content.value = "Primero selecciona una carpeta de destino."
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
                                    ft.ElevatedButton("Cargar imagen con fondo", on_click=cargar_imagen, tooltip="Selecciona una imagen para quitar el fondo")
                                ]
                            ),
                            ft.Row(
                                [
                                    ft.ElevatedButton("Procesar carpeta de imágenes", on_click=seleccionar_carpeta_imagenes, tooltip="Selecciona una carpeta con imágenes para quitarles el fondo"),
                                  ]
                            )
                        ],
                        alignment=ft.MainAxisAlignment.START,
                        horizontal_alignment=ft.CrossAxisAlignment.CENTER,
                    ),
                    padding=container_padding,
                ),
                # Segunda columna con barra de progreso centrada y vista previa de imagen sin fondo
                ft.Container(
                    content=ft.Column(
                        [
                            
                            ft.Text("Vista previa de la imagen sin fondo:", weight=ft.FontWeight.BOLD),
                            removed_bg_image_preview,
                            ft.Row(
                                [
                                    ft.ElevatedButton("Seleccionar carpeta destino", on_click=seleccionar_carpeta_destino, tooltip="Selecciona una carpeta de destino"),
                                ]
                            ),
                            ft.Row(
                                [
                                    ft.ElevatedButton("Abrir carpeta destino", on_click=abrir_carpeta_destino_click, tooltip="Abrir la carpeta de destino seleccionada")
                                ]
                            ),
                            ft.Column(
                                [
                                    progress_text,  # Texto de progreso (inicialmente oculto)
                                    progress  # Barra de progreso (inicialmente oculta)
                                ],
                                alignment=ft.MainAxisAlignment.CENTER,
                                horizontal_alignment=ft.CrossAxisAlignment.CENTER,
                            )
                        ],
                        alignment=ft.MainAxisAlignment.CENTER,
                        horizontal_alignment=ft.CrossAxisAlignment.CENTER,
                    ),
                    padding=container_padding,
                )
            ],
            alignment=ft.MainAxisAlignment.SPACE_EVENLY
        ),
        snack_bar,
    )

    # Crear el icono en la bandeja del sistema
    create_tray_icon(page)
    
ft.app(target=main, view=ft.AppView.FLET_APP, assets_dir='assets')