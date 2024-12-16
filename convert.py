import os
import sys
import io
from typing import BinaryIO
from formats.docx.docx import convert_docx_to_pdf
from formats.xlsx.xlsx import convert_xlsx_to_pdf
from formats.pptx.pptx import convert_pptx_to_pdf
from formats.images.images import convert_image_to_pdf
from formats.txt.txt import convert_txt_to_pdf
from flask import jsonify

def download_pdf():
    return os.path.join(os.path.expanduser('~'), 'Downloads')

def generate_unique_filename(base_path, base_name, extension):
    counter = 1
    new_path = os.path.join(base_path, f"{base_name}{extension}")
    while os.path.exists(new_path):
        new_path = os.path.join(base_path, f"{base_name}_{counter}{extension}")
        counter += 1
    return new_path

def convert_file_to_pdf(input_path: str, output_path: str = "") -> str:
    try:
        ext = os.path.splitext(input_path)[1].lower()
        base_name = os.path.splitext(os.path.basename(input_path))[0]

        downloads = download_pdf()
        output_path = generate_unique_filename(downloads, base_name, '.pdf')

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
        else:
            raise ValueError(f"INVALID_FILE_FORMAT: {ext}")

        print(f"Archivo PDF generado en: {output_path}")
        return output_path


    except Exception as e:
        error_message = f"CONVERSION_ERROR: {str(e)}"
        print(error_message)
        raise ValueError(error_message)

# def convert_file_buffer_to_pdf(file_buffer: BinaryIO, filename: str) -> bytes:
#     """
#     Convierte un archivo en buffer (stream) a PDF y devuelve el PDF como bytes.

#     :param file_buffer: Archivo en buffer (BinaryIO o BytesIO).
#     :param filename: Nombre del archivo original para identificar su tipo.
#     :return: El PDF generado como bytes.
#     """
#     file_extension = filename.lower().split('.')[-1]
#     output_buffer = io.BytesIO()  # Donde almacenaremos el PDF generado

#     try:
#         if file_extension == "docx":
#             # Convertir DOCX a PDF
#             convert_docx_to_pdf(file_buffer, output_buffer)
#         elif file_extension == "xlsx":
#             # Convertir XLSX a PDF
#             convert_xlsx_to_pdf(file_buffer, output_buffer)
#         elif file_extension == "pptx":
#             # Convertir PPTX a PDF
#             convert_pptx_to_pdf(file_buffer, output_buffer)
#         elif file_extension in ["png", "jpg", "jpeg", "svg"]:
#             # Convertir imágenes a PDF
#             convert_image_to_pdf(file_buffer, output_buffer)
#         elif file_extension == "txt":
#             # Convertir TXT a PDF
#             convert_txt_to_pdf(file_buffer, output_buffer)
#         else:
#             raise ValueError(f"Formato de archivo no soportado: {file_extension}")
#     except Exception as e:
#         raise ValueError(f"Error al convertir archivo: {e}")

#     # Retornar el PDF generado como bytes
#     output_buffer.seek(0)
#     return output_buffer.read()

if __name__ == '__main__':
    if len(sys.argv) < 2:
        print("Uso: python script.py <ruta_del_archivo>")
        sys.exit(1)

    input_file = sys.argv[1]

    try:
        pdf_path = convert_file_to_pdf(input_file)
        print(f"PDF generado en: {pdf_path}")
    except Exception as e:
        print(f"Error: {str(e)}")