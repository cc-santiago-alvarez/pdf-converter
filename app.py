import os
import tempfile
from flask import Flask, request, jsonify, send_file, render_template
from flask_cors import CORS
from convert import convert_file_to_pdf

app = Flask(__name__)
CORS(app, resources={r"/api/*": {"origins": "*"}})  # Asegúrate de permitir el origen necesario
app.config['CORS_HEADERS'] = 'Content-Type'

# Carpeta temporal para almacenar archivos
TEMP_FOLDER = "./temp/"
os.makedirs(TEMP_FOLDER, exist_ok=True)

@app.route('/')
def home():
    return render_template('index.html')

@app.route('/api/v1/convert/convert-to-pdf', methods=['POST'])
def convert():
    try:
        if 'file' not in request.files:
            return jsonify({'error': 'No se encontró el campo "file".'}), 400

        uploaded_file = request.files['file']
        input_path = os.path.join(TEMP_FOLDER, uploaded_file.filename)
        uploaded_file.save(input_path)

        output_path = convert_file_to_pdf(input_path)

        if not isinstance(output_path, str):
            raise ValueError(f"La función convert_file_to_pdf devolvió un valor inesperado: {output_path}")

        file_url = f"http://{request.host}/download/{os.path.basename(output_path)}"
        return jsonify({'success': True, 'pdf_url': file_url})

    except Exception as e:
        return jsonify({'error': str(e)}), 500


@app.route('/download/<filename>', methods=['GET'])
def download_file(filename):
    try:

        file_path = os.path.join(TEMP_FOLDER, filename)

        if not os.path.exists(file_path):
            return jsonify({'error': 'Archivo no encontrado'}), 404

        print(f"Enviando archivo: {file_path}", flush=True)

        return send_file(file_path, as_attachment=True)

    except Exception as e:
        return jsonify({'error': str(e)}), 500


if __name__ == '__main__':
    app.run(debug=True, host='10.2.20.113', port=25268)