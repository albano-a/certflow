import streamlit as st
import pandas as pd
from PIL import Image, ImageDraw, ImageFont
import os
import zipfile
from io import BytesIO
import locale
from functions import draw_bounding_box

st.set_page_config(
    page_title="Gerador de Certificados", layout="centered", page_icon="🦈"
)


st.title("Gerador de Certificados")

st.subheader("📄 Modelo de certificado")

template_options = ["evento_3instituicoes", "modelo1", "modelo1"]
template = st.selectbox(
    "Selecione o modelo de certificado:",
    template_options,
)
template = "templates/" + template + ".png"

if template:
    with st.expander("Preview do modelo"):
        st.subheader("Preview do Modelo de Certificado")
        st.image(template, caption="Modelo de Certificado", use_container_width=True)


planilha = st.file_uploader("Planilha de participantes (.xlsx)", type=["xlsx"])

if planilha:
    with st.expander("Preview da planilha"):
        try:
            df_preview = pd.read_excel(planilha)
            df_preview = df_preview.drop_duplicates()
            st.dataframe(df_preview)
        except Exception as e:
            st.error(f"Erro ao carregar a planilha: {e}")


title_font = "fonts/CormorantGaramond-Bold.ttf"
text_font = "fonts/LibreBaskerville-Bold.ttf"
name_font = "fonts/AlexBrush-Regular.ttf"

HEIGHT_EVENT = ""
HEIGHT_MINI = ""

event_name = st.text_input("Nome do Evento", value="Evento1")
hour = st.text_input("Carga horária (ex.: 8 horas)", value="0 horas")
locale.setlocale(locale.LC_TIME, "pt_BR.UTF-8")
date = st.date_input(
    "Insira a data do evento", value="today", format="DD/MM/YYYY"
).strftime("%d de %B de %Y")




if template and planilha:
    with st.expander("Gerar certificados"):
        df = pd.read_excel(planilha)
        df = df.drop_duplicates()
        img_template = Image.open(template)
        font_name = ImageFont.truetype(name_font, size=85)
        font_event = ImageFont.truetype(text_font, size=55)
        font_hour = ImageFont.truetype(text_font, size=40)
        font_date = ImageFont.truetype(text_font, size=25)

        certificates = []
        preview_image = None

        for idx, row in df.iterrows():
            nome = row["nome"]
            novo_cert = img_template.copy()
            draw = ImageDraw.Draw(novo_cert)
            # Puts the name on the template
            draw_bounding_box(
                draw, 
                novo_cert, 
                nome, 
                font_name, 
                424
            )

            # Puts the event on the template
            draw_bounding_box(
                draw, 
                novo_cert, 
                event_name, 
                font_event, 
                630
            )
            
            draw_bounding_box(
                draw, 
                novo_cert, 
                hour, 
                font_hour, 
                769
            )
            
            full_date = "Niterói, " + date
            draw_bounding_box(
                draw, 
                novo_cert, 
                full_date, 
                font_date, 
                898
            )

            certificates.append(novo_cert)

            if idx == 0:  # Save the first certificate for preview
                preview_image = novo_cert.copy()

        st.success(f"{len(df)} certificados gerados com sucesso!")

        # Display preview of the first certificate
        if certificates:
            st.subheader("Preview dos Certificados")

            # Controles do carrossel
            current_idx = st.selectbox(
                "Selecione o certificado:",
                range(len(certificates)),
                format_func=lambda x: f"{df.iloc[x]['nome']} ({x + 1}/{len(certificates)})",
            )

            # Exibir certificado atual
            st.image(
                certificates[current_idx],
                caption=f"Certificado de {df.iloc[current_idx]['nome']}",
                use_container_width=True,
            )

        # Create a ZIP file for download
        zip_buffer = BytesIO()
        with zipfile.ZipFile(zip_buffer, "w") as zipf:
            for idx, cert in enumerate(certificates):
                nome = df.iloc[idx]["nome"]
                nome_arquivo = f"{nome.replace(' ', '_')}.pdf"
                pdf_buffer = BytesIO()
                cert.convert("RGB").save(pdf_buffer, "PDF")
                zipf.writestr(nome_arquivo, pdf_buffer.getvalue())

        zip_buffer.seek(0)
        st.download_button(
            label="Baixar todos os certificados (ZIP)",
            data=zip_buffer,
            file_name="certificados.zip",
            mime="application/zip",
        )
