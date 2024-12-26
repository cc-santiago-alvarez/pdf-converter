import pypandoc

def convert_txt_to_pdf(input_path: str, output_path: str) -> None:
    """
    Convierte un archivo TXT al formato PDF.

    Parámetros:
    - input_path (str): Ruta del archivo TXT de entrada.
    - output_path (str): Ruta donde se generará el archivo PDF.

    Retorna:
    - None.
    """
    with open(input_path, 'r', encoding='utf-8') as f:
        content = f.read()
    pypandoc.convert_text(content, 'pdf', format='markdown', outputfile=output_path)