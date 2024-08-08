import logging
import os

from jinja2 import Environment, FileSystemLoader
from weasyprint import HTML
import qrcode
from io import BytesIO
import base64

# WeasyPrint va unga bog'liq modullar loglarini o'chirish
for logger_name in ['weasyprint', 'fontTools', 'PIL']:
    logger = logging.getLogger(logger_name)
    logger.setLevel(logging.CRITICAL)
    logger.propagate = False


async def generate_qr_code(data):
    qr = qrcode.QRCode(
        version=1,
        error_correction=qrcode.constants.ERROR_CORRECT_L,
        box_size=10,
        border=4,
    )
    qr.add_data(data)
    qr.make(fit=True)
    img = qr.make_image(fill_color="black", back_color="white")
    buffered = BytesIO()
    img.save(buffered, format="PNG")
    img_str = base64.b64encode(buffered.getvalue()).decode()
    return img_str


async def generate_pdf(pdf_data, *args, **kwargs):
    template_path = 'data/templates/'
    template_name = 'html_template.html'
    env = Environment(loader=FileSystemLoader(template_path))
    template = env.get_template(template_name)

    pdf_data.update({'qrCode': await generate_qr_code(f"https://admission.usat.uz/contract-info2024/{pdf_data.get('contractId', 'unknown')}")})

    html_out = template.render(pdfData=pdf_data)

    output_path_template = 'data/contacts/'
    if not os.path.exists(output_path_template):
        os.makedirs(output_path_template)
    output_path = f"{output_path_template}{pdf_data.get('fullName', 'unknown')}.pdf"
    HTML(string=html_out, base_url=template_path).write_pdf(output_path)

    return output_path
