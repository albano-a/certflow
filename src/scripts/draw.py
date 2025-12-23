import os
import zipfile
from datetime import datetime
from io import BytesIO

import pandas as pd
import streamlit as st
from PIL import Image, ImageDraw, ImageFont
from PIL.ImageFont import truetype


fonts = {
    "title_font": "fonts/CormorantGaramond-Bold.ttf",
    "text_font": "fonts/LibreBaskerville-Bold.ttf",
    "date_font": "fonts/LibreBaskerville-Regular.ttf",
    "name_font": "fonts/AlexBrush-Regular.ttf",
}


class DrawCertificate:
    def __init__(self, draw_obj, certificate):
        self.draw_obj = draw_obj
        self.certificate = certificate
        self.fs_common = 40
        self.fs_title = 85
        self.fs_date = 25

        self.name_font = truetype(fonts["name_font"], size=self.fs_title)
        self.common_font = truetype(fonts["text_font"], size=self.fs_common)
        self.date_font = truetype(fonts["date_font"], size=self.fs_date)

    def draw_text(self, text: str, ftype: str, hposition: int):
        """Draws text in the middle of the page"""
        # Puts the name on the template
        if hposition is None:
            return

        font_dict = {
            "Name": self.name_font,
            "Common": self.common_font,
            "Date": self.date_font,
        }

        bbox = self.draw_obj.textbbox((0, 0), text, font=font_dict[ftype])
        w = bbox[2] - bbox[0]
        h = bbox[3] - bbox[1]
        pos = ((self.certificate.width - w) // 2, hposition)
        self.draw_obj.text(pos, text, font=font_dict[ftype], fill="black")
