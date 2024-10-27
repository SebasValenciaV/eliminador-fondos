## Aplicación para eliminar el fondo de una imagen

![eliminar-fondos](https://github.com/user-attachments/assets/7683c257-738d-4a14-b675-37105b185cde)

- Aplicación creada con Python y Flet para seleccionar una imagen y eliminar el fondo.Este proyecto permite eliminar el fondo de imágenes y buscar imágenes gratuitas a través de diferentes motores de búsqueda. Utiliza la biblioteca [Flet](https://flet.dev/) para la interfaz gráfica y [rembg](https://github.com/danielgatis/rembg) para la eliminación de fondos.

## Características

- **Eliminar Fondos**: Permite cargar imágenes o seleccionar carpetas enteras para eliminar el fondo de las imágenes. Las imágenes procesadas se guardan en una carpeta de destino especificada.
- **Buscador de Imágenes**: Ofrece una ventana independiente para buscar imágenes gratuitas utilizando varios motores de búsqueda (Unsplash, Pexels y Pixabay).
- **Interfaz Amigable**: Interfaz gráfica intuitiva y fácil de usar.

## Requisitos

- Python 3.7 o superior
- Las siguientes bibliotecas:
  - `flet`
  - `rembg`
  - `Pillow`
  - `pystray`

El programa debería instalar de forma automática las dependencias ejecutando:

```
python3 run_app.py
```

Puedes instalar las dependencias necesarias utilizando pip:

```
pip install flet rembg Pillow pystray
```

Uso

![fondo-eliminado](https://github.com/user-attachments/assets/26f6e6a3-a296-45ca-b7bd-59298b0c795b)

    Eliminar Fondos:
        Abre la aplicación.
        Selecciona una imagen o una carpeta con imágenes.
        Especifica una carpeta de destino.
        Haz clic en "Procesar" para eliminar los fondos de las imágenes seleccionadas.

    Buscar Imágenes:
        Haz clic en "Buscador de Imágenes" en el menú.
        Introduce el término de búsqueda y selecciona un motor de búsqueda.
        Haz clic en "Buscar" para abrir los resultados en tu navegador web.

Estructura del Proyecto
```
/Eliminar-fondos
│
├── main.py                # Archivo principal de la aplicación
├── buscador.py            # Módulo para el buscador de imágenes
├── menu.py                # Módulo para el menú de la aplicación
├── assets/                # Carpeta para iconos y recursos
│   └── tray-icon.png      # Icono para la bandeja del sistema
│   └── default-image.png  # Imagen de que no hay imágenes cargadas en el proyecto
└── requirements.txt       # Archivo con las dependencias del proyecto
```
Contribuciones

Las contribuciones son bienvenidas. Si deseas contribuir, por favor crea un fork del repositorio y envía un pull request con tus cambios.

Licencia

Este proyecto está bajo GPL-3.0 license.


