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
    try:
        if 'file[0]' not in request.files:
            return jsonify({'error': 'No se encontró el campo "file".'}), 400
         
        results = []
        count =0
        
        for _, uploaded_file in request.files.items():
             
            count += 1 
            print(f"Procesando archivo {count}: {uploaded_file.filename}")
           
            original_filename = uploaded_file.filename
            
            originalName = os.path.splitext(original_filename)[0]
            
            extension = '.pdf'
            
            input_path = io.BytesIO(uploaded_file.read()) 
            pdf_buffer = convert_file_to_pdf(input_path, original_filename)
            
            pdf_buffer.seek(0)  # Reiniciar el puntero del archivo
            pdf_bytes = list(pdf_buffer.read())
            
            results.append({
                'file': pdf_bytes,
                'originalName': f"{originalName}{extension}"
            })
            
            
             # Retornar la respuesta con los archivos procesados
        return jsonify({
            'success': True,
            'count': len(results),  # Cantidad de archivos procesados
            'files': results
        })
        
        
    except Exception as e:
        print("Error:", str(e))
        return jsonify({'error': str(e)}), 500

            
        
        # if not isinstance(output_path, str):
        #     raise ValueError(f"La función convert_file_to_pdf devolvió un valor inesperado: {output_path}")
        
        # # Leer el archivo convertido como bytes
        # with open(output_path, 'rb') as pdf_file:
        #     pdf_bytes = pdf_file.read()
            
        #     results.append(
        #      {
        #         'file': list(pdf_bytes),
        #         'originalName': f"{originalName}{extension}",
        #     }
        #     )
            
            # print("sisas----------------->",results)

    #     return jsonify({ 
    #         'success': True,
    #         'files': results
    #     })
     
    # except Exception as e:
    #     return jsonify({'error': str(e)}), 500

       
if __name__ == '__main__':
    app.run(debug=True, host='10.2.20.113', port=25268)

