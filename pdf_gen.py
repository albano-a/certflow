from reportlab.lib.pagesizes import A4, landscape
from reportlab.pdfgen import canvas
from reportlab.lib.colors import HexColor
from reportlab.lib.units import cm
from io import BytesIO

def gerar_pdf(nome, evento, data):
    buffer = BytesIO()
    w, h = landscape(A4)
    c = canvas.Canvas(buffer, pagesize=landscape(A4))

    c.setFillColor(HexColor("#FFFFFF"))
    c.rect(0, 0, w, h, fill=1)

    c.setFillColor(HexColor("#FF6F61"))  # laranja vibrante
    c.circle(w * 0.8, h * 0.7, 100, fill=1, stroke=0)

    c.setFillColor(HexColor("#6A1B9A"))  # roxo escuro
    c.rect(w * 0.1, h * 0.2, 200, 120, fill=1, stroke=0)

    c.setFont("Helvetica-Bold", 48)
    c.setFillColor(HexColor("#4A148C"))  # roxo escuro para texto
    c.drawCentredString(w / 2, h - 4 * cm, "Certificado de Participação")

    c.setFont("Helvetica", 26)
    c.setFillColor(HexColor("#212121"))  # quase preto
    c.drawCentredString(w / 2, h - 7 * cm, "Certificamos que")

    c.setFont("Helvetica-Bold", 30)
    c.setFillColor(HexColor("#FF6F61"))  # laranja no nome pra destaque
    c.drawCentredString(w / 2, h - 9 * cm, nome)

    c.setFont("Helvetica", 26)
    c.setFillColor(HexColor("#212121"))
    c.drawCentredString(w / 2, h - 11 * cm, "participou do evento")

    c.setFont("Helvetica-Bold", 28)
    c.setFillColor(HexColor("#6A1B9A"))  # roxo
    c.drawCentredString(w / 2, h - 13 * cm, evento)

    c.setFont("Helvetica", 22)
    c.setFillColor(HexColor("#212121"))
    c.drawCentredString(w / 2, h - 16 * cm, f"realizado em {data}")

    c.setStrokeColor(HexColor("#6A1B9A"))
    c.setLineWidth(1.5)
    c.line(w - 8 * cm, 3 * cm, w - 2 * cm, 3 * cm)

    c.setFont("Helvetica", 16)
    c.drawString(w - 7.8 * cm, 2.5 * cm, "Organizador")

    c.showPage()
    c.save()
    buffer.seek(0)
    return buffer.read()
