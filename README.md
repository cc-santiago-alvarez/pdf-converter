# PDF Converter

Aplicación Flask para conversión de archivos (DOCX, XLSX, PPTX, TXT, imágenes) a PDF.

## Requisitos del Sistema

### Dependencias de Sistema

#### Linux (Debian/Ubuntu)

```bash
sudo apt-get install -y \
    python3-dev \
    libcairo2-dev \
    libpango1.0-dev \
    libgdk-pixbuf2.0-dev \
    libffi-dev \
    libxml2-dev \
    libxslt-dev \
    libjpeg-dev \
    zlib1g-dev \
    libgtk-3-dev
```

#### macOS

```bash
brew install cairo pango gdk-pixbuf libffi libxml2 libxslt jpeg
```

#### Windows

1. Instalar [GTK+ Runtime](https://github.com/tschoonj/GTK-for-Windows-Runtime-Environment-Installer/releases)
2. Instalar [Visual Studio Build Tools](https://visualstudio.microsoft.com/visual-cpp-build-tools/) (seleccionar "Desktop development with C++")

### Dependencias de Python

```bash
pip3 install -r requirements.txt
```
#### Si no funciona pip install -r requirements.txt
```bash
pip3 install Pillow reportlab openpyxl python-pptx svglib flask flask-cors python-docx weasyprint lxml
```

## Instalación y Uso

### 1. Clonar Repositorio

```bash
git clone https://github.com/tu-usuario/salvarsa-pdf-converter.git
cd salvarsa-pdf-converter
```

### 2. Configurar Entorno Virtual

```bash
# Linux/macOS
python3 -m venv venv
source venv/bin/activate

# Windows
python -m venv venv
.\venv\Scripts\activate
```

### 3. Instalar Dependencias

```bash
pip install --upgrade pip
pip install -r requirements.txt

# Instalación adicional para conversión de TXT (requiere Node.js)
pip install pypandoc
```

### 4. Iniciar Servidor Flask

```bash
# Linux/macOS
export FLASK_APP=app.py
flask run --host=0.0.0.0 --port=25268

# Windows
set FLASK_APP=app.py
flask run --host=0.0.0.0 --port=25268
```

## Estructura del Proyecto

```
salvarsa-pdf-converter/
├── app.py                # Punto de entrada principal
├── convert.py            # Lógica central de conversión
├── requirements.txt      # Dependencias de Python
├── formats/              # Módulos de conversión específicos
│   ├── docx/             # Conversión de Word
│   ├── images/           # Conversión de imágenes
│   ├── pptx/             # Conversión de PowerPoint
│   ├── txt/              # Conversión de texto plano
│   └── xlsx/             # Conversión de Excel
├── static/               # Archivos estáticos
└── templates/            # Plantillas HTML
```

## Uso de la API

### Endpoint Principal

```
POST /api/v1/convert/convert-to-pdf
```

### Parametros(opcional)

   - Content-Type: application/pdf
   - Content-Disposition: attachment; filename="archivo.pdf"


### Ejemplo con cURL

```bash
curl -X POST -F "file=@documento.docx" http://localhost:25268/api/v1/convert/convert-to-pdf
```

## Conversión de Formatos Soportados

| Formato    | Extensiones Soportadas  |
| ---------- | ----------------------- |
| Word       | .docx                   |
| Excel      | .xlsx                   |
| PowerPoint | .pptx                   |
| Texto      | .txt                    |
| Imágenes   | .png, .jpg, .jpeg, .svg |

## Solución de Problemas

### Errores Comunes

1. **Faltan dependencias de sistema**:

   - Verificar instalación de Cairo/Pango
   - Reinstalar dependencias con `sudo apt-get install --reinstall libcairo2 libpango-1.0-0`

2. **Problemas con WeasyPrint**:

   ```bash
   pip uninstall weasyprint
   pip install --no-cache-dir weasyprint
   ```

3. **Conversión de imágenes en Windows**:

   - Asegurar que las DLLs de GTK+ están en el PATH del sistema

### Modo de Depuración

Iniciar la aplicación con:

```bash
FLASK_DEBUG=1 flask run --host=0.0.0.0 --port=25268
```
