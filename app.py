from flask import Flask, request, render_template, jsonify
from flask_cors import CORS
from convert import convert_file_to_pdf


app = Flask(__name__)
CORS(app, resources={r"/*": {"origins": "http://10.2.20.120:8063"}})

@app.route('/')
def home():
    return render_template('index.html')

@app.route('/api/v1/convert/convert-to-pdf', methods=['POST'])
def convert():
    try:
        uploaded_file = request.files['file']
        if not uploaded_file:
            return jsonify({'error': 'No se proporcionó ningún archivo.'}), 400
        
        # Guardar el archivo temporalmente
        input_path = f"./static/{uploaded_file.filename}"
        uploaded_file.save(input_path)
        
        output_path = convert_file_to_pdf(input_path, "")
        
        response = (jsonify({'success': True, 'pdf_path': output_path}))
        response.headers['Access-Control-Allow-Origin'] = 'http://localhost:8063'  # Origen permitido
        return response
    except Exception as e:
        response = (jsonify({'error': str(e)}), 500)
        response.headers['Access-Control-Allow-Origin'] = 'http://localhost:8063'
        return response

if __name__ == '__main__':
    app.run(debug=True, host='10.2.20.113', port=25268)
#api/v1/convert/convert-to-pdf