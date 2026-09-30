from PIL import Image, ImageDraw, ImageFont
import os

FONT_PATH = "assets/fonts/Montserrat.ttf"

def get_font(size):
    try:
        return ImageFont.truetype(FONT_PATH, size)
    except:
        return ImageFont.load_default()

def draw_on_screen_text(draw, text, y=880, is_dark_bg=False, strike_through=False, font_size=48):
    """
    Renderiza texto na tela rigorosamente de acordo com as regras:
    - Sans-serif geométrica em negrito (Montserrat)
    - Sempre em caixa alta
    - No máximo 5 palavras
    """
    if not text:
        return
        
    words = text.strip().split()
    if len(words) > 5:
        words = words[:5]
    display_text = " ".join(words).upper()
    
    font = get_font(font_size)
    bbox = font.getbbox(display_text)
    tw = bbox[2] - bbox[0]
    th = bbox[3] - bbox[1]
    
    x = (1920 - tw) // 2
    
    # Fundo sutil do card de texto (pill transparente para legibilidade perfeita)
    pad_x = 36
    pad_y = 16
    card_bg = (15, 23, 42, 220) if not is_dark_bg else (245, 241, 234, 235)
    text_color = (255, 255, 255) if not is_dark_bg else (20, 33, 61)
    
    # Desenha texto com sombra suave para destaque
    draw.text((x + 2, y + 2), display_text, fill=(0, 0, 0, 80), font=font)
    draw.text((x, y), display_text, fill=text_color, font=font)
    
    if strike_through:
        line_y = y + th // 2 + 5
        draw.line([x - 15, line_y, x + tw + 15, line_y], fill=(209, 73, 91), width=6)
