import os
import io
import tempfile
import base64
from werkzeug.datastructures import FileStorage
from flask import Flask, request, jsonify, send_file, render_template, url_for
from flask_cors import CORS
from convert import convert_file_to_pdf

app = Flask(__name__)
CORS(app, resources={r"/api/*": {"origins": "*"}})  # Asegúrate de permitir el origen necesario
app.config['CORS_HEADERS'] = 'Content-Type'


@app.route('/')
def home():
    return render_template('index.html')

@app.route('/api/v1/convert/convert-to-pdf', methods=['POST'])
def convert():
    VALID_EXTENSIONS = ['.docx', '.xlsx', '.pptx', '.txt', '.png', '.jpg', '.jpeg', '.svg']

    try:
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
                    'file': list(pdf_buffer),
                    'originalName': f"{original_name}.pdf"
                })

            finally:
                os.remove(temp_file_path)
                if pdf_output_path and os.path.exists(pdf_output_path):
                    os.remove(pdf_output_path)

        return jsonify({
            'success': True,
            'count': len(results),
            'files': results
        })

    except Exception as e:
        print("Error:", str(e))
        return jsonify({'error': str(e)}), 500

def convert_pdf_to_buffer(pdf_path: str) -> bytes:
    try:
        with open(pdf_path, 'rb') as pdf_file:
            return pdf_file.read()
    except Exception as e:
        raise ValueError(f"ERROR_READING_PDF: {e}")


       
if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0', port=25268)