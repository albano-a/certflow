import zipfile
from datetime import datetime
from io import BytesIO

import pandas as pd
import streamlit as st
from PIL import Image, ImageDraw
from scripts.draw import DrawCertificate


def capitalize_mes(data_str):
    partes = data_str.split(" de ")
    if len(partes) == 2:
        return f"{partes[0]} de {partes[1].capitalize()}"
    return data_str.capitalize()


def preview_planilha(planilha):
    """Preview the uploaded spreadsheet."""
    try:
        df_preview = pd.read_excel(planilha)
        df_preview = df_preview.drop_duplicates()
        st.dataframe(df_preview)
        return df_preview
    except Exception as e:
        st.error(f"Erro ao carregar a planilha: {e}")
        return None


def gerar_certificados(
    df,
    template,
    positions,
    event_type,
    event_name,
    professor,
    hour,
    start_end_date,
    date,
    start_date=None,
    end_date=None,
):
    """Generate certificates based on the provided data and template."""
    img_template = Image.open(template)

    certificates = []
    preview_image = None

    for idx, row in df.iterrows():
        nome = row["nome"]
        novo_cert = img_template.copy()
        draw = ImageDraw.Draw(novo_cert)
        dc = DrawCertificate(draw, novo_cert)

        dc.draw_text(nome, "Name", positions[event_type]["NAME_HEIGHT"])
        dc.draw_text(event_name, "Common", positions[event_type]["EVENT_NAME_HEIGHT"])
        dc.draw_text(
            professor, "Common", positions[event_type]["PROFESSOR_MINI_HEIGHT"]
        )

        if start_end_date == "Único dia":
            dc.draw_text(
                hour,
                "Common",
                positions[event_type]["CARGA_HORARIA_HEIGHT"],
            )
            # Now, for the location and date
            full_date = "Niterói, " + date
            dc.draw_text(
                full_date,
                "Date",
                positions[event_type]["LOCATION_HEIGHT"],
            )
        else:
            dc.draw_text(
                f"{start_date.capitalize()} à {end_date.capitalize()}",
                "Common",
                positions[event_type]["DATA_VARIOS_DIAS"],
            )
            dc.draw_text(
                hour,
                "Common",
                positions[event_type]["CARGA_HORARIA_VARIOS_DIAS"],
            )
            full_date = datetime.today().strftime("Niterói, %d de %B de %Y")
            dc.draw_text(
                full_date,
                "Date",
                positions[event_type]["LOCATION_HEIGHT_VARIOS_DIAS"],
            )

        certificates.append(novo_cert)
        if idx == 0:
            preview_image = novo_cert.copy()

    return certificates, preview_image


def criar_zip(certificates, df):
    """Create a ZIP file containing all certificates in PDF format."""
    zip_buffer = BytesIO()
    with zipfile.ZipFile(zip_buffer, "w") as zipf:
        for idx, cert in enumerate(certificates):
            nome = df.iloc[idx]["nome"]
            nome_arquivo = f"{nome.replace(' ', '_')}.pdf"
            pdf_buffer = BytesIO()
            cert.convert("RGB").save(pdf_buffer, "PDF")
            zipf.writestr(nome_arquivo, pdf_buffer.getvalue())
    zip_buffer.seek(0)
    return zip_buffer
