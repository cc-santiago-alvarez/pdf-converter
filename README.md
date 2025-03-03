# PDF Converter API

API REST para conversión de documentos a PDF, compatible con múltiples formatos. Desarrollada con Flask y Python.

## 📋 Características
- Conversión a PDF desde: DOCX, XLSX, PPTX, TXT, HTML, SVG, PNG, JPG/JPEG
- Soporte para múltiples archivos en una sola solicitud
- Generación directa de PDF o respuesta JSON con base64
- Conversión desde HTML almacenado en MongoDB
- Interfaz web básica para pruebas

## 🛠 Prerrequisitos
- Python 3.8+
- MongoDB (para conversión desde base de datos)
- Librerías de sistema:
  - **Debian/Ubuntu**:  
    `sudo apt-get install python3-dev libcairo2 libpango-1.0-0 libpangocairo-1.0-0 libgdk-pixbuf2.0-0 libffi-dev shared-mime-info`
  - **macOS** (via Homebrew):  
    `brew install cairo pango gdk-pixbuf libffi`
  - **Windows**:  
    Descargar GTK+ Runtime de [gtk.org](https://gtk.org/download/)

## 🚀 Instalación

### 1. Clonar repositorio
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

### Endpoint principal
- para convertir los formatos [DOCX, XLSX, PPTX, TXT, SVG, PNG, JPG]
```bash
POST /api/v1/convert/convert-to-pdf
```

**Parámetros:**
- `file`: Archivo(s) a convertir (form-data)
- `responseType` (query param):  
  - `json` (default): Devuelve JSON con base64  
  - `file`: Devuelve PDF directamente

**Ejemplo de solicitud (Postman):**
1. Método: POST
2. URL: `http://localhost:25268/api/v1/convert/convert-to-pdf?responseType=file`
3. Body -> form-data:
   - Key: `file` (tipo File)
   - Seleccionar archivo

**Respuesta exitosa (JSON):**
```json
{
  "success": true,
  "count": 1,
  "files": [
    {
      "file": [base64_string],
      "originalName": "documento"
    }
  ]
}
```

### Conversión desde MongoDB
- para convertir los formato HTML
```bash
GET /api/v1/convert/from-db/<document_id>
```

## 🖥 Interfaz Web
Accede a `http://localhost:25268` para:
- Subir archivos mediante formulario
- Descarga directa del PDF convertido

![Interfaz web](screenshots/web-interface.png)

## 🐛 Solución de problemas

### Errores Comunes

1. **Faltan dependencias de sistema**:
   - Síntoma: Errores con `weasyprint` o `cairo`
   - Solución: Instalar librerías listadas en prerrequisitos
   - Solución: en la ruta donde se instan las librerías en macOS
   ```bash
   export DYLD_LIBRARY_PATH=/opt/homebrew/lib:$DYLD_LIBRARY_PATH
   ```

2. **Problemas con MongoDB**:
   - Verificar conexión en `db.py`
   - Asegurar que MongoDB está corriendo en `localhost:27017`

3. **Formato no soportado**:
   - Verificar extensiones permitidas: `.docx, .xlsx, .pptx, .txt, .png, .jpg, .jpeg, .svg, .html, .htm`

### Logs de error
Los errores se muestran en consola con detalle completo. Ejemplo:
```log
Error: CONVERSION_ERROR: Invalid file format: .odt
```

## 📄 Notas técnicas

### Estructura del proyecto
```
salvarsa-pdf-converter/
├── app.py                # Punto de entrada principal
├── convert.py            # Lógica central de conversión
├── db.py                 # Conexión a MongoDB
├── requirements.txt      # Dependencias Python
├── formats/              # Convertidores específicos por formato
├── static/               # Archivos estáticos (CSS)
└── templates/            # Plantillas HTML
```

### Dependencias clave
| Paquete         | Uso                              |
|-----------------|----------------------------------|
| Flask           | Servidor web y manejo de rutas   |
| WeasyPrint      | Conversión HTML/CSS a PDF        |
| python-docx     | Lectura de archivos DOCX         |
| openpyxl        | Procesamiento de archivos XLSX   |
| python-pptx     | Manipulación de archivos PPTX    |
| reportlab       | Generación de PDFs complejos     |
| pymongo         | Conexión con MongoDB             |

## 🤝 Contribución
1. Haz fork del proyecto
2. Crea tu rama: `git checkout -b feature/nueva-funcionalidad`
3. Haz commit: `git commit -m 'Add some feature'`
4. Push: `git push origin feature/nueva-funcionalidad`
5. Abre un Pull Request

## 📄 Licencia
MIT License - Ver [LICENSE](LICENSE)
