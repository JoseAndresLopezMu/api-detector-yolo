
# API de Detección de Objetos con YOLOv10 y Docker

Este proyecto proporciona una API RESTful construida con FastAPI y empaquetada con Docker para realizar la detección de objetos (personas y coches) en imágenes utilizando el modelo YOLOv10.

## Características

- **Modelo Eficiente**: Utiliza YOLOv10, una de las arquitecturas más recientes y eficientes para la detección de objetos en tiempo real.
- **API Rápida**: Construida sobre FastAPI, lo que garantiza un alto rendimiento y una documentación interactiva automática.
- **Totalmente Dockerizada**: El entorno está completamente contenido en una imagen de Docker, asegurando una configuración y despliegue sencillos y consistentes.
- **Configuración Sencilla**: La instalación de dependencias y la ejecución se gestionan con un único conjunto de comandos de Docker.

## Requisitos Previos

Antes de comenzar, asegúrate de tener instalado y en funcionamiento **Docker Desktop** en tu sistema.

> **Descargar Docker**  
> Asegúrate de que el motor de Docker esté en ejecución antes de proceder con los siguientes pasos.

## Estructura del Proyecto

```
.
├── api-detector-yolo-car/
│   ├── Dockerfile          # Define los pasos para construir la imagen de Docker.
│   ├── pyproject.toml      # Define las dependencias de Python.
│   ├── main.py             # Lógica de la API con FastAPI.
│   ├── object_detector.py  # Encapsula la lógica del modelo YOLOv10.
│   ├── config.py           # Gestiona la configuración (modelo, confianza, etc.).
│   ├── schemas.py          # Define los esquemas de datos para las peticiones y respuestas.
│   └── .dockerignore       # Especifica qué archivos ignorar al construir la imagen.
└── README.md               # Esta guía.
```

## Guía de Instalación y Ejecución

Sigue estos pasos para poner en marcha la API en tu máquina local.

### Paso 1: Clona o Descarga el Repositorio

Asegúrate de tener todos los archivos del proyecto en una carpeta en tu ordenador.

### Paso 2: Construye la Imagen de Docker

Abre una terminal, navega hasta la carpeta raíz del proyecto (la que contiene el `Dockerfile`) y ejecuta el siguiente comando. Este comando creará una imagen de Docker llamada `yolo-api` con todas las dependencias necesarias.

```bash
docker build -t yolo-api .
```

> **Nota:** La primera vez que construyas la imagen, el proceso puede tardar varios minutos mientras se descargan las capas base y se instalan las dependencias.

### Paso 3: Ejecuta el Contenedor

Una vez que la imagen se haya construido correctamente, puedes iniciar un contenedor a partir de ella con el siguiente comando:

```bash
docker run --name yolo-container -p 8000:8000 yolo-api
```

**Desglose del comando:**

- `--name yolo-container`: Asigna un nombre fácil de recordar al contenedor.
- `-p 8000:8000`: Mapea el puerto 8000 de tu máquina al puerto 8000 del contenedor.
- `yolo-api`: El nombre de la imagen que quieres ejecutar.

> Si todo ha ido bien, verás un mensaje en la terminal indicando que el servidor Uvicorn está funcionando.  
> **Nota:** La primera vez que ejecutes el contenedor, este descargará automáticamente los pesos del modelo `yolov10n.pt`.

## Gestión de Contenedores y Errores Comunes

### Error: `The container name "/yolo-container" is already in use`

Este error ocurre si intentas ejecutar el comando `docker run` después de que un contenedor con el mismo nombre ya haya sido creado (incluso si está detenido).

Tienes dos soluciones:

#### 1. Iniciar el contenedor existente

```bash
docker start yolo-container
```

#### 2. Eliminar el contenedor antiguo y crear uno nuevo

Este es el método recomendado si has hecho cambios en el código y has reconstruido la imagen.

```bash
docker rm yolo-container
docker run --name yolo-container -p 8000:8000 yolo-api
```

## Cómo Usar la API

Con el contenedor en ejecución, la API está lista para recibir peticiones.

### 1. Usando la Documentación Interactiva (Recomendado)

La forma más sencilla de probar la API es a través de la documentación automática de Swagger UI.

Abre tu navegador web y ve a:  
👉 **http://localhost:8000/docs**

Desde allí, podrás ver el endpoint `/detectar/`, desplegarlo, hacer clic en "Try it out", seleccionar un archivo de imagen de tu ordenador y ejecutar la detección.

### 2. Usando cURL (Línea de Comandos)

Si prefieres usar la terminal, puedes enviar una petición POST con un comando como `curl`. Asegúrate de tener una imagen de prueba (ej: `mi_imagen.jpg`) en la misma carpeta desde la que ejecutas el comando.

```bash
curl -X POST -F "image_file=@mi_imagen.jpg" http://localhost:8000/detectar/
```

## Respuesta de la API

Si la detección es exitosa, recibirás una respuesta en formato JSON similar a esta:

```json
{
  "detecciones": [
    {
      "objeto": "person",
      "confianza": 0.85,
      "coordenadas": [150.5, 230.0, 250.5, 480.0]
    },
    {
      "objeto": "car",
      "confianza": 0.92,
      "coordenadas": [400.0, 310.2, 650.8, 450.5]
    }
  ]
}
```

## Detener el Contenedor

Para detener la aplicación, simplemente ve a la terminal donde se está ejecutando el contenedor y presiona `CTRL + C`.

> Esto solo detiene el contenedor, no lo elimina.  
> Para volver a lanzarlo, consulta la sección **"Gestión de Contenedores"**.
