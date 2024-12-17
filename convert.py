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

def convert_file_to_pdf(input_path: BinaryIO, filename: str) -> io.BytesIO:
    try:
        # ext = os.path.splitext(input_path)[1].lower()
        # base_name = os.path.splitext(os.path.basename(input_path))[0]

        # downloads = download_pdf()
        # output_path = generate_unique_filename(downloads, base_name, '.pdf')
        ext = os.path.splitext(filename)[1].lower()
        pdf_buffer = io.BytesIO()  # Crear un buffer en memoria para el PDF

        if ext == '.docx':
            convert_docx_to_pdf(input_path, pdf_buffer)
        elif ext == '.xlsx':
            convert_xlsx_to_pdf(input_path, pdf_buffer)
        elif ext == '.pptx':
            convert_pptx_to_pdf(input_path, pdf_buffer)
        elif ext == '.txt':
            convert_txt_to_pdf(input_path, pdf_buffer)
        elif ext in ['.svg', '.png', '.jpg', '.jpeg']:
            convert_image_to_pdf(input_path, pdf_buffer)
        else:
            raise ValueError(f"INVALID_FILE_FORMAT: {ext}")

        print(f"Archivo PDF generado en: {pdf_buffer}")
        return pdf_buffer


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