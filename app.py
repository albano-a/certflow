import streamlit as st
import pandas as pd
import pdf_gen as pg
import zipfile
from io import BytesIO

st.title("Gerador de Certificados")

uploaded_file = st.file_uploader("Envie a planilha Excel", type=["xlsx"])

if uploaded_file:
    df = pd.read_excel(uploaded_file)

    df = st.data_editor(df)

    zip_buffer = BytesIO()
    with zipfile.ZipFile(zip_buffer, "a") as zipf:
        for _, row in df.iterrows():
            pdf_bytes = pg.gerar_pdf(row["nome"], row["evento"], row["data"])
            zipf.writestr(f"{row['nome']}_certificado.pdf", pdf_bytes)

    st.download_button(
        "Baixar certificados (ZIP)",
        data=zip_buffer.getvalue(),
        file_name="certificados.zip",
        mime="application/zip",
    )
