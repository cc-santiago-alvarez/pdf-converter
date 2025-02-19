from weasyprint import HTML, CSS
import tempfile

def convert_html_to_pdf(html_content: str) -> str:
    """Convierte HTML a PDF respetando estilos originales + formato A4"""
    try:
        a4_css = """
        <style>
            @page {
                size: A4;
                margin: 0;
            }
            
            body {
               padding: 0.5cm;
            }
            
            .content-wrapper {
                width: 100%;
                height: 100%;
               
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

        with tempfile.NamedTemporaryFile(delete=False, suffix=".pdf") as temp_pdf:
            output_path = temp_pdf.name
        
        HTML(string=full_html).write_pdf(
            output_path,
            presentational_hints=True,
            stylesheets=[
                CSS(string='''
                    /* Reset básico compatible */
                    * {{
                        max-width: 100% !important;
                        /*box-sizing: border-box !important;*/
                    }}
                ''')
            ]
        )
        
        return output_path
        
    except Exception as e:
        raise ValueError(f"HTML_CONVERSION_ERROR: {str(e)}")