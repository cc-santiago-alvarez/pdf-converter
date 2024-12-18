# import io
# from openpyxl import load_workbook
# from reportlab.lib import colors
# from reportlab.lib.pagesizes import letter, landscape
# from reportlab.platypus import SimpleDocTemplate, Table, TableStyle, Paragraph, Image, Spacer
# from reportlab.lib.units import inch
# from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
# from reportlab.lib.enums import TA_CENTER, TA_LEFT
# from openpyxl.utils import get_column_letter
# from reportlab.lib.units import cm
    
# def get_column_widths(sheet, max_width):
    
#     column_widths = []
#     for col in sheet.columns:
#         width = sheet.column_dimensions[col[0].column_letter].width
#         if width is None:
#             width = 10
#         column_widths.append(width * 8)
    
#     total_width = sum(column_widths)
#     if total_width > max_width:
#         scale = max_width / total_width
#         column_widths = [width * scale for width in column_widths]
    
#     return column_widths

# def get_row_heights(sheet, max_height=50):
#     row_heights = []
#     for row in sheet.iter_rows():
#         height = sheet.row_dimensions[row[0].row].height
#         if height is None:
#             height = 15
#         if height > max_height: 
#             height = max_height
#         row_heights.append(height)
        
#     return row_heights

# # Función para procesar celdas y ajustarlas a tamaños de hoja
# def process_cell(cell, centered_style, max_characters=100):
#     if cell.data_type == 'i':  # Image
#         img = Image(io.BytesIO(cell.value))
#         img.drawHeight = 50  
#         img.drawWidth = 50 
#         return img
#     elif cell.value is not None:
#         cell_value = str(cell.value)
#         if len(cell_value) > max_characters: 
#             cell_value = cell_value[:max_characters] + '...'  # Truncar contenido largo
#         return Paragraph(cell_value, centered_style)
#     return ''


# def convert_xlsx_to_pdf(input_path: str, output_path: str) -> None:
#     wb = load_workbook(input_path)
#     sheet = wb.active

#     sheet_width = 0
#     for column in sheet.columns:
#         col_letter = get_column_letter(column[0].column)
#         col_width = sheet.column_dimensions[col_letter].width
#         if col_width is None:
#             col_width = 8.43  # Ancho predeterminado en Excel (8.43 caracteres)
#         sheet_width += col_width
    
#     sheet_height = 0
#     for row in sheet.rows:
#         row_height = sheet.row_dimensions[row[0].row].height
#         if row_height is None:
#             row_height = 15  
#         sheet_height += row_height

#     # Convertir las dimensiones a puntos (1 punto = 1/72 pulgadas)
#     page_width = sheet_width * 0.35  # Aproximación de unidades de Excel a cm
#     page_height = sheet_height * 0.035  # Aproximación de unidades de Excel a cm

#     margin_left = 0.2 * cm
#     margin_right = 0.2 * cm
#     margin_top = 0.5 * cm
#     margin_bottom = 0.5 * cm

#     pdf = SimpleDocTemplate(
#         output_path,
#         pagesize=(page_width * cm, page_height * cm),
#         leftMargin=margin_left,
#         rightMargin=margin_right,
#         topMargin=margin_top,
#         bottomMargin=margin_bottom
#     )

#     data = []
#     styles = getSampleStyleSheet()
#     centered_style = ParagraphStyle('centered', parent=styles['Normal'], alignment=TA_CENTER, wordWrap='CJK')
    
#     for row in sheet.iter_rows():
#         processed_row = []
#         for cell in row:
#             processed_cell = process_cell(cell, centered_style)
#             processed_row.append(processed_cell)
#         data.append(processed_row)

#     column_widths = get_column_widths(sheet, page_width * cm - (margin_left + margin_right))

#     table = Table(data, colWidths=column_widths, repeatRows=1)

#     style = TableStyle([
#         ('GRID', (0, 0), (-1, -1), 1, colors.black),
#         ('VALIGN', (0, 0), (-1, -1), 'MIDDLE'),
#         ('ALIGN', (0, 0), (-1, -1), 'CENTER'),
#         ('LEFTPADDING', (0, 0), (-1, -1), 3),
#         ('RIGHTPADDING', (0, 0), (-1, -1), 3),
#         ('TOPPADDING', (0, 0), (-1, -1), 3),
#         ('BOTTOMPADDING', (0, 0), (-1, -1), 3),
#         ('BACKGROUND', (0, 0), (-1, 0), colors.lightgrey),
#         ('FONTSIZE', (0, 0), (-1, -1), 8),
#     ])

#     # Combinar celdas
#     for merged_range in sheet.merged_cells.ranges:
#         min_col, min_row, max_col, max_row = merged_range.bounds
#         style.add('SPAN', (min_col - 1, min_row - 1), (max_col - 1, max_row - 1))

#     table.setStyle(style)
#     elements = [table]

#     try:
#         pdf.build(elements)
#     except Exception as e:
#         raise ValueError(f"CONVERTION_ERROR: {e}")
import os
import io
import zipfile
from xml.etree import ElementTree as ET
from reportlab.lib import colors
from reportlab.platypus import SimpleDocTemplate, Table, TableStyle, Paragraph, Spacer
from reportlab.lib.pagesizes import letter, landscape
from reportlab.lib.units import cm
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
from reportlab.lib.enums import TA_CENTER

NAMESPACE = {'ns': 'http://schemas.openxmlformats.org/spreadsheetml/2006/main'}


def extract_xlsx_xml(input_path: str):
    """
    Extrae y procesa los archivos XML de un archivo .xlsx.

    Args:
        input_path (str): Ruta del archivo .xlsx.

    Returns:
        dict: Diccionario con las rutas relativas de los archivos XML y sus contenidos como árboles XML.
    """
    xml_files = {}
    with zipfile.ZipFile(input_path, 'r') as xlsx:
        for file_name in xlsx.namelist():
            if file_name.endswith('.xml'):
                with xlsx.open(file_name) as xml_file:
                    tree = ET.parse(xml_file)
                    xml_files[file_name] = tree
    return xml_files


def parse_sheet(sheet_tree):
    """
    Procesa el XML de una hoja de cálculo para extraer los valores de las celdas.

    Args:
        sheet_tree (ElementTree): Árbol XML de la hoja.

    Returns:
        list: Lista de filas, donde cada fila es una lista de valores de celdas.
    """
    root = sheet_tree.getroot()
    rows = []

    # Encontrar todas las filas en el XML
    for row in root.findall('ns:sheetData/ns:row', NAMESPACE):
        row_data = []
        for cell in row.findall('ns:c', NAMESPACE):
            cell_value = cell.find('ns:v', NAMESPACE)
            row_data.append(cell_value.text if cell_value is not None else "")
        rows.append(row_data)

    return rows


def get_shared_strings(xml_files):
    """
    Obtiene las cadenas compartidas desde el archivo `sharedStrings.xml`.

    Args:
        xml_files (dict): Diccionario con los archivos XML del .xlsx.

    Returns:
        list: Lista de cadenas compartidas.
    """
    shared_strings = []
    shared_strings_file = xml_files.get('xl/sharedStrings.xml')
    if shared_strings_file:
        root = shared_strings_file.getroot()
        for si in root.findall('ns:si', NAMESPACE):
            t_element = si.find('ns:t', NAMESPACE)
            shared_strings.append(t_element.text if t_element is not None else "")
    return shared_strings


def process_cell(value, centered_style, max_characters=100):
    """
    Procesa una celda de Excel para convertirla a un objeto compatible con ReportLab.

    Args:
        value (str): Valor de la celda.
        centered_style (ParagraphStyle): Estilo del párrafo.
        max_characters (int): Número máximo de caracteres por celda.

    Returns:
        Paragraph: Objeto ReportLab para la celda procesada.
    """
    if value is not None:
        value = value.strip()
        if len(value) > max_characters:
            value = value[:max_characters] + '...'
        return Paragraph(value, centered_style)
    return ''


def convert_xlsx_to_pdf(input_path: str, output_path: str) -> None:
    xml_files = extract_xlsx_xml(input_path)

    shared_strings = get_shared_strings(xml_files)

    sheets_data = {}
    for file_name, tree in xml_files.items():
        if file_name.startswith('xl/worksheets/sheet'):
            sheet_name = file_name.split('/')[-1].replace('.xml', '')
            sheets_data[sheet_name] = parse_sheet(tree)

    styles = getSampleStyleSheet()
    centered_style = ParagraphStyle(
        'centered', parent=styles['Normal'], alignment=TA_CENTER, wordWrap='CJK'
    )

    # Crear documento PDF
    pdf = SimpleDocTemplate(
        output_path,
        pagesize=landscape(letter),
        leftMargin=1 * cm,
        rightMargin=1 * cm,
        topMargin=1 * cm,
        bottomMargin=1 * cm
    )

    elements = []

    for sheet_name, rows in sheets_data.items():
        data = []

        # Recorrer las filas de la hoja y procesar las celdas
        for row in rows:
            processed_row = [
                process_cell(shared_strings[int(cell)] if cell.isdigit() else cell, centered_style)
                for cell in row
            ]
            data.append(processed_row)

        # Crear tabla para la hoja
        column_count = max(len(row) for row in data) if data else 0
        column_widths = [6 * cm] * column_count  # Ancho de columna fijo

        table = Table(data, colWidths=column_widths)

        # Estilo de la tabla
        style = TableStyle([
            ('GRID', (0, 0), (-1, -1), 1, colors.black),
            ('VALIGN', (0, 0), (-1, -1), 'MIDDLE'),
            ('ALIGN', (0, 0), (-1, -1), 'CENTER'),
            ('BACKGROUND', (0, 0), (-1, 0), colors.lightgrey),
            ('FONTSIZE', (0, 0), (-1, -1), 8),
        ])
        table.setStyle(style)

        # Agregar tabla y salto de página
        elements.append(Paragraph(f"Hoja: {sheet_name}", styles['Heading2']))
        elements.append(table)
        elements.append(Spacer(1, 12))

    try:
        pdf.build(elements)
    except Exception as e:
        raise ValueError(f"CONVERSION_ERROR: {e}")
