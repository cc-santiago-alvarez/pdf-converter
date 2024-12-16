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

# Carpeta temporal para almacenar archivos
TEMP_FOLDER = "./temp/"
os.makedirs(TEMP_FOLDER, exist_ok=True)

@app.route('/')
def home():
    return render_template('index.html')

@app.route('/api/v1/convert/convert-to-pdf', methods=['POST'])
def convert():
    try:
        if 'file[0]' not in request.files:
            return jsonify({'error': 'No se encontró el campo "file".'}), 400
        

        uploaded_file = request.files['file[0]']
        extension = '.pdf'
        original_filename = uploaded_file.filename
        originalName = os.path.splitext(original_filename)[0]
        input_path = os.path.join(TEMP_FOLDER, uploaded_file.filename)
        uploaded_file.save(input_path)
        
        output_path = convert_file_to_pdf(input_path)
        
        if not isinstance(output_path, str):
            raise ValueError(f"La función convert_file_to_pdf devolvió un valor inesperado: {output_path}")
        
        # Leer el archivo convertido como bytes
        with open(output_path, 'rb') as pdf_file:
            pdf_bytes = pdf_file.read()

        return jsonify({ 
            'success': True,
            'files': [{
                'file': list(pdf_bytes),
                'originalName': f"{originalName}{extension}",
            }]
        })
    except Exception as e:
        return jsonify({'error': str(e)}), 500

if __name__ == '__main__':
    app.run(debug=True, host='10.2.20.113', port=25268)
