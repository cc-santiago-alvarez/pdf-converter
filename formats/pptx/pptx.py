from pptx import Presentation
from reportlab.pdfgen import canvas
from reportlab.lib.colors import HexColor
from io import BytesIO
from PIL import Image as PILImage
from formats.pptx.pptx_fonts import extract_text_properties, get_shape_position
from reportlab.lib.styles import ParagraphStyle
from reportlab.platypus import Paragraph
from reportlab.lib.enums import TA_LEFT, TA_CENTER, TA_RIGHT, TA_JUSTIFY
from reportlab.lib.colors import black
from reportlab.lib.units import inch

def extract_image_from_shape(shape, pdf, slide_height):
    """
    Extrae imágenes de un shape de PowerPoint y las dibuja en el PDF.

    Parámetros:
    - shape: Forma de la diapositiva de PowerPoint.
    - pdf: Objeto Canvas para generar el PDF.
    - slide_height: Altura de la diapositiva en puntos.

    Retorna:
    - None.
    """
    if shape.shape_type == 13:  # Si el shape es una imagen.
        img_stream = BytesIO(shape.image.blob)  # Obtiene los datos binarios de la imagen.
        img = PILImage.open(img_stream) 
        left, top, width, height = get_shape_position(shape, slide_height)
        pdf.drawInlineImage(img, left, top - height, width, height)


def extract_background_image(slide):
    """
    Extrae la imagen de fondo de una diapositiva, si existe.

    Parámetros:
    - slide: Objeto de la diapositiva de PowerPoint.

    Retorna:
    - PIL.Image: Imagen de fondo.
    - None: Si no hay fondo.
    """
    background = slide.background
    if background.fill.type == 6:  # Verifica si el fondo tiene una imagen.
        image = background.fill.picture.image
        image_stream = BytesIO(image.blob)  # Obtiene los datos binarios de la imagen.
        return PILImage.open(image_stream)  # Retorna la imagen como un objeto PIL.
    return None

def extract_table_from_shape(shape):
    """
    Extrae los datos de una tabla de un shape de PowerPoint.

    Parámetros:
    - shape: Forma que contiene una tabla.

    Retorna:
    - list[list[str]]: Lista de filas con celdas como cadenas de texto.
    - None: Si el shape no contiene una tabla.
    """
    if shape.has_table:
        table_data = []
        for row in shape.table.rows:
            row_data = [cell.text for cell in row.cells]
            table_data.append(row_data)
        return table_data
    return None

def draw_text_with_properties(pdf, text_props, left, top, width, height):
    """
    Dibuja texto en el PDF con las propiedades específicas de texto.

    Parámetros:
    - pdf: Objeto Canvas del PDF.
    - text_props: Lista de propiedades del texto (fuente, tamaño, color, etc.).
    - left, top: Coordenadas de la posición inicial del texto.
    - width, height: Ancho y alto del área de texto.

    Retorna:
    - float: Posición vertical actual después de dibujar el texto.
    """
    total_height = sum(prop.get('font_size', 12) * 1.2 for prop in text_props)
    current_y = top
    
    # Ajusta la posición vertical según la alineación.
    vertical_alignment = text_props[0].get('vertical_alignment', 0)
    if vertical_alignment == 1:  # Middle
        current_y = top - (height - total_height) / 2
    elif vertical_alignment == 2:  # Bottom
        current_y = top - height + total_height
    
    # Itera sobre las propiedades y dibuja cada párrafo.
    for prop in text_props:
        font_name = prop.get('font_name', 'Helvetica')
        if prop.get('bold') and prop.get('italic'):
            font_name += '-BoldOblique'
        elif prop.get('bold'):
            font_name += '-Bold'
        elif prop.get('italic'):
            font_name += '-Oblique'

        alignment = TA_LEFT
        if prop.get('alignment') == 1:
            alignment = TA_CENTER
        elif prop.get('alignment') == 2:
            alignment = TA_RIGHT
        elif prop.get('alignment') == 3:
            alignment = TA_JUSTIFY

        text_color = black
        if 'color' in prop:
            try:
                text_color = HexColor(prop['color'])
            except ValueError:
                print(f"Warning: Invalid color value '{prop['color']}'. Using black instead.")

        font_size = prop.get('font_size', 12)
        style = ParagraphStyle(
            name='Custom',
            fontName=font_name,
            fontSize=font_size,
            textColor=text_color,
            alignment=alignment,
            leading=font_size * 1.2
        )

        para = Paragraph(prop.get('text', ''), style)
        para.wrapOn(pdf, width, height)  # Ajusta el texto dentro del ancho/alto disponibles.
        para.drawOn(pdf, left, current_y - para.height)
        current_y -= para.height  # Actualiza la posición vertical.

    return current_y

def convert_pptx_to_pdf(input_path: str, output_path: str):
    """
    Convierte un archivo PPTX al formato PDF.

    Parámetros:
    - input_path (str): Ruta del archivo PPTX de entrada.
    - output_path (str): Ruta donde se generará el archivo PDF.

    Retorna:
    - None.

    Lanza:
    - ValueError: Si ocurre un error durante la conversión.
    """
    prs = Presentation(input_path) 
    slide_width = prs.slide_width / 914400 * inch  # Convierte el ancho de la diapositiva a puntos.
    slide_height = prs.slide_height / 914400 * inch  # Convierte la altura de la diapositiva a puntos.
    pdf = canvas.Canvas(output_path, pagesize=(slide_width, slide_height))
    
    for slide in prs.slides:
        fill = slide.background.fill
        if fill.type == 1:  # Solid fill
            bg_color = f"#{fill.fore_color.rgb:06x}"
            pdf.setFillColor(HexColor(bg_color))
            pdf.rect(0, 0, slide_width, slide_height, fill=1)

        for shape in slide.shapes:
            if shape.has_text_frame:
                text_props = extract_text_properties(shape, slide.element.xml, slide.part.slide.element.nsmap)
                if text_props:
                    left, top, width, height = get_shape_position(shape, slide_height)
                    draw_text_with_properties(pdf, text_props, left, top, width, height)
            elif shape.shape_type == 13:  # Picture
                extract_image_from_shape(shape, pdf, slide_height)
        
        pdf.showPage() # Crea una nueva página en el PDF.
    
    pdf.save() # Guarda el archivo PDF.