import os
import io
import tempfile
import base64
from werkzeug.datastructures import FileStorage
from flask import Flask, request, jsonify, send_file, render_template, url_for, Response
from flask_cors import CORS
from convert import convert_file_to_pdf

app = Flask(__name__)

# Configura CORS para permitir solicitudes desde cualquier origen en los endpoints de la API
CORS(app, resources={r"/api/*": {"origins": "*"}})  # Asegúrate de permitir el origen necesario
app.config['CORS_HEADERS'] = 'Content-Type'


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
    VALID_EXTENSIONS = ['.docx', '.xlsx', '.pptx', '.txt', '.png', '.jpg', '.jpeg', '.svg']

    try:
        # Obtiene el tipo de respuesta esperado (JSON por defecto o archivo directo)
        response_type =  request.args.get('responseType', 'json')
        cond_response_file = response_type == 'file[0]'

        if 'file[0]' not in request.files:
            return jsonify({'error': 'No se encontró el campo "file".'}), 400

        results = []
        count = 0

        for _, uploaded_file in request.files.items():
            count += 1
            print(f"Procesando archivo {count}: {uploaded_file.filename}")

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
                    'originalName': f"{original_name}.pdf"
                })

            finally:
                # Elimina el archivo temporal original
                os.remove(temp_file_path)
                if pdf_output_path and os.path.exists(pdf_output_path):
                    os.remove(pdf_output_path)
        
        # Si se solicita como archivo, retorna el PDF directamente
        if cond_response_file:
            return Response(
                results[0].get('file'),
                mimetype="application/pdf;charset=UTF-8",
                headers={
                    "Access-Control-Allow-Origin": "*",
                    "Content-Type": "application/pdf;charset=UTF-8",
                    "Content-Disposition": 'inline; filename=' + results[0].get('originalName'),
                    "Content-Transfer-Encoding": 'binary'
                },
                status=201
            )

        return jsonify({
            'success': True,
            'count': len(results),
            'files': results
        })

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


       
if __name__ == '__main__':
    # Ejecuta el servidor Flask en modo de depuración
    app.run(debug=True, host='0.0.0.0', port=25268)