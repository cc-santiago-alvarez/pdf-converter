import os
import tempfile
import sys
from formats.docx.docx import convert_docx_to_pdf
from formats.xlsx.xlsx import convert_xlsx_to_pdf
from formats.pptx.pptx import convert_pptx_to_pdf
from formats.images.images import convert_image_to_pdf
from formats.txt.txt import convert_txt_to_pdf

def convert_file_to_pdf(input_path: str) -> str:
    """
    Convierte un archivo al formato PDF.

    Parámetros:
    - input_path (str): Ruta del archivo a convertir.

    Retorna:
    - str: Ruta del archivo PDF generado.

    """
    try:
        ext = os.path.splitext(input_path)[1].lower()  # Obtén la extensión del archivo
        base_name = os.path.splitext(os.path.basename(input_path))[0]
        
        # Crea un archivo temporal para el PDF de salida
        with tempfile.NamedTemporaryFile(delete=False, suffix=".pdf") as temp_pdf:
            output_path = temp_pdf.name

        if ext == '.docx':
            convert_docx_to_pdf(input_path, output_path)
        elif ext == '.xlsx':
            convert_xlsx_to_pdf(input_path, output_path)
        elif ext == '.pptx':
            convert_pptx_to_pdf(input_path, output_path)
        elif ext == '.txt':
            convert_txt_to_pdf(input_path, output_path)
        elif ext in ['.svg', '.png', '.jpg', '.jpeg']:
            convert_image_to_pdf(input_path, output_path)
        elif ext in ['.html', '.htm']:
            convert_txt_to_pdf(input_path, output_path)
        else:
            raise ValueError(f"INVALID_FILE_FORMAT: {ext}")

        print(f"Archivo PDF generado en: {output_path}")
        return output_path  # Devuelve la ruta del archivo temporal

    except Exception as e:
        error_message = f"CONVERSION_ERROR: {str(e)}"
        print(error_message)
        raise ValueError(error_message)

if __name__ == '__main__':
    if len(sys.argv) < 2:
        print("Uso: python script.py <ruta_del_archivo>")
        sys.exit(1)

    input_file = sys.argv[1]

    # Llama a la función de conversión y obtiene la ruta del PDF
    try:
        pdf_path = convert_file_to_pdf(input_file)
        print(f"PDF generado en: {pdf_path}")
    except Exception as e:
        print(f"Error: {str(e)}")
