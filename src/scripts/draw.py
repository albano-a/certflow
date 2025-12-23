def draw_bounding_box(draw_obj, certificado, text, font, hposition):
    """Draws text in the middle of the page"""
    # Puts the name on the template
    bbox = draw_obj.textbbox((0, 0), text, font=font)
    w = bbox[2] - bbox[0]
    h = bbox[3] - bbox[1]
    pos = ((certificado.width - w) // 2, hposition)
    draw_obj.text(pos, text, font=font, fill="black")
