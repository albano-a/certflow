import locale

from datetime import datetime
from scripts.utils import (
    capitalize_mes,
    preview_planilha,
    gerar_certificados,
    criar_zip,
)
import streamlit as st


# --- Streamlit UI ---
st.set_page_config(
    page_title="Gerador de Certificados", layout="centered", page_icon="🦈"
)
st.title("Gerador de Certificados")
st.subheader("📄 Modelo de certificado")

event_type = st.radio(
    "É um evento ou um Minicurso/Papo Geofísico?",
    ["Evento", "Minicurso"],
    horizontal=True,
)

template_options = (
    ["Evento - Único", "Evento - 3 Instituições", "Evento - Único - Vários Dias"]
    if event_type == "Evento"
    else ["Minicurso", "Minicurso - Vários Dias", "Papo Geofísico"]
)
template = st.selectbox(
    "Selecione o modelo de certificado:",
    template_options,
)
template = "templates/" + template + ".png"

if template:
    with st.expander("Preview do modelo"):
        st.subheader("Preview do Modelo de Certificado")
        st.image(template, caption="Modelo de Certificado")

event_name = st.text_input(
    "Nome do Evento",
    placeholder="Ex.: Semana da Geofísica, Mesa Redonda, Workshop...",
    max_chars=100,
)
professor = ""
if event_type == "Minicurso":
    professor = st.text_input(
        "Ministrante do Minicurso ou Apresentador do Papo Geofísico", value="Professor"
    )
hour = st.text_input(
    "Carga horária (ex.: 8 horas)", placeholder="Ex.: 4 horas, 2 horas...", max_chars=20
)

start_end_date = st.radio(
    "O evento ocorreu em um único dia ou em vários dias?",
    ["Único dia", "Vários dias"],
    index=0,
    horizontal=True,
)
date, start_date, end_date = None, None, None
if start_end_date == "Único dia":
    date = st.date_input(
        "Data do evento",
        value=datetime.today(),
        format="DD/MM/YYYY",
        max_value=datetime.today(),
    ).strftime("%d de %B de %Y")
else:
    cols = st.columns(2)
    locale.setlocale(locale.LC_TIME, "pt_BR.UTF-8")
    with cols[0]:
        start_date = capitalize_mes(
            st.date_input(
                "Data de início do evento",
                value=datetime.today(),
                format="DD/MM/YYYY",
            ).strftime("%d de %B")
        )
    with cols[1]:

        end_date = capitalize_mes(
            st.date_input(
                "Data final do evento",
                value=datetime.today(),
                format="DD/MM/YYYY",
            ).strftime("%d de %B")
        )

planilha = st.file_uploader("Planilha de participantes (.xlsx)", type=["xlsx"])
df = None
if planilha:
    with st.expander("Preview da planilha"):
        df = preview_planilha(planilha)


POSITIONS = {
    "Evento": {
        "NAME_HEIGHT": 375,
        "EVENT_NAME_HEIGHT": 520,
        "PROFESSOR_MINI_HEIGHT": None,
        "CARGA_HORARIA_HEIGHT": 635,
        "DATA_VARIOS_DIAS": 626,
        "CARGA_HORARIA_VARIOS_DIAS": 732,
        "LOCATION_HEIGHT": 698,
        "LOCATION_HEIGHT_VARIOS_DIAS": 809,
    },
    "Minicurso": {
        "NAME_HEIGHT": 375,
        "EVENT_NAME_HEIGHT": 520,
        "PROFESSOR_MINI_HEIGHT": 642,
        "CARGA_HORARIA_HEIGHT": 763,
        "DATA_VARIOS_DIAS": 701,
        "CARGA_HORARIA_VARIOS_DIAS": 822,
        "LOCATION_HEIGHT": 826,
        "LOCATION_HEIGHT_VARIOS_DIAS": 885,
    },
}

if template and df is not None:
    with st.expander("Gerar certificados"):
        certificates, preview_image = gerar_certificados(
            df,
            template,
            POSITIONS,
            event_type,
            event_name,
            professor,
            hour,
            start_end_date,
            date,
            start_date,
            end_date,
        )
        st.success(f"{len(df)} certificados gerados com sucesso!")

        if certificates:
            st.subheader("Preview dos Certificados")
            current_idx = st.selectbox(
                "Selecione o certificado:",
                range(len(certificates)),
                format_func=lambda x: f"{df.iloc[x]['nome']} ({x + 1}/{len(certificates)})",
            )
            st.image(
                certificates[current_idx],
                caption=f"Certificado de {df.iloc[current_idx]['nome']}",
            )

        zip_buffer = criar_zip(certificates, df)
        st.download_button(
            label="Baixar todos os certificados (ZIP)",
            data=zip_buffer,
            file_name="certificados.zip",
            mime="application/zip",
        )
