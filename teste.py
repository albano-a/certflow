import pdf_gen as pg
import zipfile
from io import BytesIO


zip_buffer = BytesIO()
with zipfile.ZipFile(zip_buffer, "a") as zipf:
    pdf_bytes = pg.gerar_pdf("João da Silva", "Curso de Python Avançado", "01/01/2024")
    zipf.writestr(f"{['nome']}_certificado.pdf", pdf_bytes)