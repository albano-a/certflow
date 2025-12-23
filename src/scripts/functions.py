import streamlit as st
import pandas as pd
from PIL import Image, ImageDraw, ImageFont
import os
import zipfile
from io import BytesIO
import locale


def draw_bounding_box(draw_obj, certificado, text, font, hposition):
    """Draws text in the middle of the page"""
    # Puts the name on the template
    bbox = draw_obj.textbbox((0, 0), text, font=font)
    w = bbox[2] - bbox[0]
    h = bbox[3] - bbox[1]
    pos = ((certificado.width - w) // 2, hposition)
    draw_obj.text(pos, text, font=font, fill="black")


# def generate_certificates(dataframe, img_template):
#     """Generate each bounding box and generates the certificate"""
#     certificates = []
#     preview_image = None

#     for idx, row in dataframe.iterrows():
#         nome = row["nome"]
#         novo_cert = img_template.copy()

#         draw_bounding_box()
