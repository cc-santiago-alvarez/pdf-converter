from weasyprint import HTML

def convert_txt_to_pdf(input_path: str, output_path: str) -> None:
    with open(input_path, 'r', encoding='utf-8') as f:
        text = f.read()
    
    # Envolver texto en HTML básico
    html_content = f"<pre>{text}</pre>"
    
    HTML(string=html_content).write_pdf(output_path)