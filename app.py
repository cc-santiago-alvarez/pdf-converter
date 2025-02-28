import os
import io
import tempfile
import base64
from werkzeug.datastructures import FileStorage
from flask import Flask, request, jsonify, send_file, render_template, url_for, Response
from flask_cors import CORS
from convert import convert_file_to_pdf
from weasyprint import HTML, default_url_fetcher
from db import get_db_connection
from formats.html.html_convert import convert_html_to_pdf


app = Flask(__name__)

CORS(app, resources={r"/api/*": {"origins": "*"}}) 


@app.route('/')
def home():
    """
    Ruta principal que muestra la página inicial (index.html) esto es solo para pruebas.
    """
    return render_template('index.html')

@app.route('/api/v1/convert/convert-to-pdf', methods=['POST'])
def convert():
    """
    Endpoint para convertir archivos a formato PDF.

    Proceso:
    1. Recibe uno o más archivos en el cuerpo de la solicitud.
    2. Verifica que cada archivo tenga una extensión válida.
    3. Convierte cada archivo al formato PDF y lo devuelve en el formato solicitado:
        - JSON con contenido en base64.
        - Archivo PDF como respuesta si se solicita con el parámetro 'responseType=file[0]'.

    Retorna:
    - JSON con detalles de los archivos convertidos o un archivo PDF directamente.
    """
    VALID_EXTENSIONS = ['.docx', '.xlsx', '.pptx', '.txt', '.png', '.jpg', '.jpeg', '.svg', '.html', '.htm']

    try:
        response_type =  request.args.get('responseType', 'json')
        cond_response_file = response_type == 'file'

        if 'file' not in request.files:
            return jsonify({'error': 'No se encontró el campo "file".'}), 400

        results = []
        count = 0

        for _, uploaded_file in request.files.items():
            count += 1
            original_filename = uploaded_file.filename
            original_name, extension = os.path.splitext(original_filename)
            extension = extension.lower()

            if extension not in VALID_EXTENSIONS:
                return jsonify({'error': f"Formato no soportado: {extension}"}), 400

            # Crear archivo temporal con la extensión original
            with tempfile.NamedTemporaryFile(delete=False, suffix=extension) as temp_file:
                temp_file.write(uploaded_file.read())
                temp_file_path = temp_file.name

            pdf_output_path = None

            try:
                pdf_output_path = convert_file_to_pdf(temp_file_path)

                pdf_buffer = convert_pdf_to_buffer(pdf_output_path)

                results.append({
                    'file': pdf_buffer if cond_response_file else list(pdf_buffer),
                    'originalName': f"{original_name}"
                })

            finally:
                # Elimina el archivo temporal original
                os.remove(temp_file_path)
                if pdf_output_path and os.path.exists(pdf_output_path):
                    os.remove(pdf_output_path)
        
        # Si se solicita como archivo, retorna el PDF directamente
        if cond_response_file:
            pdf_buffer = results[0].get('file')
            original_name = results[0].get('originalName')

    # Forzar la descarga con el nombre correcto y MIME type
        return Response(
        pdf_buffer,
        mimetype="application/pdf",
        headers={
            "Content-Disposition": f'attachment; filename="{original_name}.pdf"',
            "Access-Control-Allow-Origin": "*",
            "Content-Type": "application/pdf;charset=UTF-8",
            "Content-Transfer-Encoding": 'binary'
        },
        status=201
    )

    except Exception as e:
        print("Error:", str(e))
        return jsonify({'error': str(e)}), 500

def convert_pdf_to_buffer(pdf_path: str) -> bytes:
    """
    Convierte un archivo PDF en un buffer de bytes para su transferencia.

    Parámetros:
    - pdf_path (str): Ruta del archivo PDF.

    Retorna:
    - bytes: Contenido binario del PDF.

    Lanza:
    - ValueError: Si ocurre un error al leer el archivo.
    """
    try:
        with open(pdf_path, 'rb') as pdf_file:
            return pdf_file.read()
    except Exception as e:
        raise ValueError(f"ERROR_READING_PDF: {e}")

@app.route('/api/v1/convert/html-to-pdf', methods=['POST'])
def convert_html():
    """
    Endpoint para convertir contenido HTML a formato PDF.

    Proceso:
    1. Recibe un payload JSON con el campo 'html_content' en el cuerpo de la solicitud.
    2. Valida la presencia y longitud mínima del contenido HTML (10 caracteres).
    3. Convierte el HTML a PDF manteniendo estilos originales y formato A4.
    4. Devuelve la respuesta según el parámetro 'responseType':
        - Archivo PDF directo si responseType=file (por defecto)
        - JSON con PDF en base64 si responseType=json

    Parámetros de consulta opcionales:
    - responseType: Tipo de respuesta (file|json). Default: file

    Retorna:
    - Respuesta HTTP con PDF como archivo descargable (por defecto)
    - JSON con estructura {
        "success": bool,
        "pdf": "base64_string" (solo si responseType=json),
        "filename": "documento.pdf"
      }

    Códigos de estado:
    - 200: Conversión exitosa
    - 400: Error en los datos de entrada
    - 500: Error interno del servidor
    """
    try:
        data = request.get_json()
        if not data or 'html_content' not in data:
            return jsonify({"error": "html_content es requerido"}), 400

        # Validar contenido HTML mínimo
        if len(data['html_content']) < 10:  # Longitud arbitraria mínima
            return jsonify({"error": "Contenido HTML inválido"}), 400

        pdf_bytes = convert_html_to_pdf(data['html_content'])
        
        return Response(
            pdf_bytes,
            mimetype="application/pdf",
            headers={
                "Content-Disposition": 'attachment; filename="documento.pdf"',
                "Access-Control-Expose-Headers": "Content-Disposition",
                "Content-Security-Policy": "default-src 'self'"
            }
        )
        
    except ValueError as e:
        return jsonify({"error": str(e)}), 400
    except Exception as e:
        return jsonify({"error": f"Error interno: {str(e)}"}), 500
       
if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0', port=25268)