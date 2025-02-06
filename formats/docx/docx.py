
import os
import shutil
import logging
import tempfile
from docx import Document
from weasyprint import HTML

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

def convert_docx_to_pdf(input_path: str, output_path: str) -> None:
    """
    Convierte un archivo DOCX a PDF con soporte para:
    - Imágenes
    - Listas y viñetas
    - Tablas
    - Alineación de texto
    """
    temp_dir = tempfile.mkdtemp()
    try:
        if not os.path.exists(input_path):
            raise FileNotFoundError(f"Archivo no encontrado: {input_path}")

        doc = Document(input_path)
        html_content = []

        base_css = """
            body { font-family: 'Arial', sans-serif; line-height: 1.6; margin: 2cm; }
            table { border-collapse: collapse; width: 100%; }
            td, th { border: 1px solid #000; padding: 8px; text-align: left; }
            img { max-width: 100%; height: auto; }
            .bold { font-weight: bold; }
            .italic { font-style: italic; }
            .underline { text-decoration: underline; }
            .justify { text-align: justify; }
            ul, ol {
                list-style-position: inside;
                padding-left: 1em;
            }
            li {
                margin: 0.3em 0;
            }
            .nested-list {
                margin-left: 2em !important;
            }
        """
        for para in doc.paragraphs:
            html_content.append(process_paragraph(para))

        for table in doc.tables:
            html_content.append(process_table(table))

        full_html = f"""
        <html>
        <head><style>{base_css}</style></head>
        <body>{''.join(html_content)}</body>
        </html>
        """
        
        HTML(string=full_html).write_pdf(output_path)
    finally:
        shutil.rmtree(temp_dir, ignore_errors=True)

def process_paragraph(para):
    """Convierte un párrafo en HTML respetando la alineación original"""
    # Mapeo de alineaciones DOCX a CSS
    alignment_map = {
        0: 'left',    # WD_ALIGN_PARAGRAPH.LEFT
        1: 'center',  # WD_ALIGN_PARAGRAPH.CENTER
        2: 'right',   # WD_ALIGN_PARAGRAPH.RIGHT
        3: 'justify'  # WD_ALIGN_PARAGRAPH.JUSTIFY
    }
    
    # Obtener alineación REAL del documento
    original_alignment = alignment_map.get(
        para.paragraph_format.alignment,
        'left'  # Valor por defecto
    )
    
    # Determinar si es lista
    is_list = any(para.style.name.startswith(t) for t in ['List Bullet', 'List Number'])
    list_type = 'ul' if 'Bullet' in para.style.name else 'ol'
    
    html = []
    
    if is_list:
        # Manejar sangría de lista
        indent = para.paragraph_format.left_indent or 0
        indent_css = f"margin-left: {indent.pt}pt;" if indent else ""
        
        html.append(
            f'<{list_type} style="list-style-position: inside; {indent_css} text-align: {original_alignment}">'
        )
        html.append(f'<li style="text-align: {original_alignment}">')  # <- ¡Alineación heredada!
    else:
        html.append(f'<p style="text-align: {original_alignment}">')
    
    # Procesar contenido (texto con estilos)
    for run in para.runs:
        text = run.text
        if not text.strip():
            continue
        
        styles = []
        if run.bold: styles.append('font-weight: bold')
        if run.italic: styles.append('font-style: italic')
        if run.underline: styles.append('text-decoration: underline')
        
        if run.font.color.rgb:
            styles.append(f'color: #{run.font.color.rgb}')
        
        span_style = '; '.join(styles)
        html.append(f'<span style="{span_style}">{text}</span>' if span_style else text)
    
    # Cerrar etiquetas adecuadamente
    if is_list:
        html.append(f'</li></{list_type}>')
    else:
        html.append('</p>')
    
    return ''.join(html)

def process_table(table):
    """Convierte una tabla en HTML."""
    html = ['<table>']
    for row in table.rows:
        html.append('<tr>')
        for cell in row.cells:
            html.append(f'<td>{" ".join(process_paragraph(p) for p in cell.paragraphs)}</td>')
        html.append('</tr>')
    html.append('</table>')
    return ''.join(html)
