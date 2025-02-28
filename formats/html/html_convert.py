from weasyprint import HTML, CSS
from io import BytesIO

def convert_html_to_pdf(html_content: str) -> bytes:
    """
    Convierte un archivo HTML en un buffer de bytes para su transferencia.

    Parámetros:
    - html_content (str): Ruta del archivo HTML.

    Retorna:
    - bytes: Contenido binario del PDF.

    Lanza:
    - ValueError: Si ocurre un error al leer el archivo.
    """
    try:
        a4_css = """
        <style>
            @page {
                size: A4;
                margin: 0;
            }
            
            body {
                margin: 0 auto !important;
                padding: 0.5cm !important;
                width: 21cm !important;  /* Ancho exacto A4 */
                min-height: 29.7cm !important;  /* Altura exacta A4 */
                font-family: Arial, sans-serif !important;
            }
            
            .content-wrapper {
                width: 100% !important;
                height: 100% !important;
                box-sizing: border-box !important;
            }
            
            /* Reset básico compatible */
            * {
                max-width: 100% !important;
                box-sizing: border-box !important;
            }
            
            img {
                max-height: 25cm !important;
                page-break-inside: avoid;
            }
            
            table {
                width: 100% !important;
                page-break-inside: auto;
            }
        </style>
        """
        
        full_html = f"""
        <!DOCTYPE html>
        <html>
            <head>{a4_css}</head>
            <body>
                <div class="content-wrapper">
                    {html_content}
                </div>
            </body>
        </html>
        """
        
        # Generar PDF en memoria
        buffer = BytesIO()
        HTML(string=full_html).write_pdf(
            buffer,
            presentational_hints=True,
            stylesheets=[
                CSS(string='''
                    /* Estilos adicionales de seguridad */
                    body > * { 
                        page-break-before: auto !important;
                        page-break-after: auto !important;
                    }
                ''')
            ]
        )
        
        return buffer.getvalue()
        
    except Exception as e:
        raise ValueError(f"HTML_CONVERSION_ERROR: {str(e)}")

# from weasyprint import HTML, CSS
# from io import BytesIO

# def convert_html_to_pdf(html_content: str) -> bytes:
#     """
#     Convierte contenido HTML a PDF preservando estilos originales y aplicando formato A4.

#     Parámetros:
#     - html_content (str): Contenido HTML a convertir

#     Retorna:
#     - bytes: PDF generado en formato binario

#     Lanza:
#     - ValueError: Si ocurre un error en el proceso de conversión
#     """
#     try:
#         # Estilos base para formato A4 (usando variables CSS y herencia)
#         a4_css = """
#         <style>
#             :root {
#                 --a4-page-width: 21cm;
#                 --a4-page-height: 29.7cm;
#                 --a4-printable-width: 19.6cm; /* 21cm - 1.4cm márgenes laterales */
#             }

#             @page {
#                 size: A4;
#                 margin: 1cm 1.4cm; /* Márgenes reales de impresión */
#             }

#             .a4-content-wrapper {
#                 width: var(--a4-printable-width) !important;
#                 min-height: var(--a4-page-height) !important;
#                 margin: 0 auto !important;
#                 padding: 0 !important;
#                 box-sizing: border-box !important;
                
#                 /* Fuerza herencia controlada */
#                 font-family: inherit;
#                 color: inherit;
#             }

#             /* Reset inteligente para contenido heredado */
#             .a4-content-wrapper > * {
#                 max-width: 100% !important;
#                 width: auto !important;
#                 margin-left: 0 !important;
#                 margin-right: 0 !important;
#                 padding: 0 !important;
#                 box-sizing: border-box !important;
#                 float: none !important;
#             }

#             /* Manejo especial para elementos críticos */
#             .a4-content-wrapper table {
#                 width: 100% !important;
#                 table-layout: auto !important;
#                 break-inside: avoid;
#             }

#             .a4-content-wrapper img {
#                 max-width: var(--a4-printable-width) !important;
#                 height: auto !important;
#                 display: block;
#                 margin: 0 auto !important;
#             }

#             .a4-content-wrapper pre {
#                 white-space: pre-wrap !important;
#                 word-wrap: break-word !important;
#             }
#         </style>
#         """

#         full_html = f"""
#         <!DOCTYPE html>
#         <html>
#             <head>{a4_css}</head>
#             <body>
#                 <div class="a4-content-wrapper">
#                     {html_content}
#                 </div>
#             </body>
#         </html>
#         """
        
#         # Configuración de conversión
#         buffer = BytesIO()
#         HTML(string=full_html).write_pdf(
#             buffer,
#             presentational_hints=True,  # Respeta atributos style inline
#             optimize_size=('fonts', 'images'),  # Optimiza sin modificar estilos
#             stylesheets=[
#                 CSS(string='''
#                     /* Reset seguro */
#                     .a4-container > * {{
#                         margin: initial !important;
#                         padding: initial !important;
#                     }}
#                 ''')
#             ]
#         )
        
#         return buffer.getvalue()
        
#     except Exception as e:
#         raise ValueError(f"Error en conversión HTML a PDF: {str(e)}")