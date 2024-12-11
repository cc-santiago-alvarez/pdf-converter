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
        

        return jsonify({'success': True, 'pdf_path': output_path}), 200
    except Exception as e:
        return jsonify({'error': str(e)}), 500

if __name__ == '__main__':
    app.run(debug=True, host='10.2.20.113', port=25268)
#api/v1/convert/convert-to-pdf