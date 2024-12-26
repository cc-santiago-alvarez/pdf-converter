import pypandoc
import pdfkit

def convert_docx_to_pdf(input_path: str, output_path: str) -> None:
    """
    Convierte un archivo DOCX al formato PDF.

    Parámetros:
    - input_path (str): Ruta del archivo DOCX de entrada.
    - output_path (str): Ruta donde se generará el archivo PDF.

    Retorna:
    - None.
    
    """
    output_path = output_path if output_path.endswith('.pdf') else output_path + '.pdf'
    try:
        # Intenta convertir directamente el archivo DOCX a PDF utilizando pypandoc.
        pypandoc.convert_file(input_path, 'pdf', outputfile=output_path, 
                              extra_args=['--pdf-engine=/Library/TeX/texbin/pdflatex'])
    except Exception as e:
        print(f"CONVERTION_ERROR: {e}")
        try:
            # Si falla, convierte primero a HTML y luego a PDF.
            html_content = pypandoc.convert_file(input_path, 'html')
            pdfkit.from_string(html_content, output_path)
        except Exception as e:
            print(f"HTML_ERROR: {e}")
            raise # Relanza el error si la conversión falla.
