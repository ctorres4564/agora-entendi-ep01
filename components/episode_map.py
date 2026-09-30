from PIL import Image, ImageDraw, ImageFont
import math
import os

FONT_PATH = "assets/fonts/Montserrat.ttf"

def get_font(size):
    try:
        return ImageFont.truetype(FONT_PATH, size)
    except:
        return ImageFont.load_default()

# Cores oficiais
COLOR_BG_LIGHT = (245, 241, 234) # #F5F1EA
COLOR_BG_DARK = (20, 33, 61)     # #14213D
COLOR_ACCENT = (242, 169, 0)     # #F2A900 (amarelo-âmbar)
COLOR_ALERT = (209, 73, 91)      # #D1495B (vermelho suave)
COLOR_TEXT_DARK = (26, 32, 44)   # Quase preto suave
COLOR_TEXT_LIGHT = (245, 245, 245)
COLOR_LINE_LIGHT = (180, 185, 195)
COLOR_LINE_DARK = (70, 90, 120)

NODES_ORDER = [
    "neurônio",
    "sinapse",
    "neurotransmissor",
    "redes",
    "plasticidade",
    "memória",
    "atenção",
    "sono"
]

def draw_mini_map(draw, active_concept, is_dark_bg=False):
    """
    Desenha o mapa do episódio compacto no canto superior direito (x: 1450 a 1870, y: 40 a 200).
    A cada conceito novo, um nó aparece com o nome e se conecta aos anteriores.
    """
    if not active_concept or active_concept not in NODES_ORDER:
        return

    active_idx = NODES_ORDER.index(active_concept)
    
    # Posições dos nós no mini mapa (2 linhas de 4 nós)
    base_x = 1420
    base_y = 50
    spacing_x = 115
    spacing_y = 55
    
    node_positions = []
    for i in range(len(NODES_ORDER)):
        row = i // 4
        col = i % 4
        x = base_x + col * spacing_x
        y = base_y + row * spacing_y
        node_positions.append((x, y))
        
    line_col = COLOR_LINE_DARK if is_dark_bg else COLOR_LINE_LIGHT
    text_col = (200, 210, 230) if is_dark_bg else (90, 100, 115)
    font = get_font(13)
    
    # Desenha conexões até o nó ativo
    for i in range(active_idx):
        p1 = node_positions[i]
        p2 = node_positions[i+1]
        draw.line([p1, p2], fill=line_col, width=2)
        
    # Conexões especiais de retorno: atenção -> memória, sono -> memória
    if active_idx >= 6: # atenção está ativo
        # Atenção (índice 6) aponta para Memória (índice 5)
        p_atencao = node_positions[6]
        p_memoria = node_positions[5]
        draw.line([p_atencao, p_memoria], fill=COLOR_ACCENT, width=2)
    if active_idx >= 7: # sono está ativo
        # Sono (índice 7) aponta para Memória (índice 5)
        p_sono = node_positions[7]
        p_memoria = node_positions[5]
        draw.line([p_sono, p_memoria], fill=COLOR_ACCENT, width=2)

    # Desenha os nós
    for i in range(active_idx + 1):
        x, y = node_positions[i]
        name = NODES_ORDER[i]
        is_current = (i == active_idx)
        
        # Cor do nó
        fill_col = COLOR_ACCENT if is_current else (line_col if not is_dark_bg else (50, 75, 110))
        border_col = (255, 255, 255) if is_dark_bg else (26, 32, 44)
        
        r = 8 if not is_current else 11
        draw.ellipse([x - r, y - r, x + r, y + r], fill=fill_col, outline=border_col, width=2)
        
        # Rótulo em caixa alta
        label = name.upper()
        bbox = font.getbbox(label)
        tw = bbox[2] - bbox[0]
        label_y = y + 12 if (i // 4 == 0) else y - 24
        draw.text((x - tw // 2, label_y), label, fill=COLOR_ACCENT if is_current else text_col, font=font)

def draw_center_map(draw, lighted_count=8, show_question_node=False):
    """
    Desenha o mapa expandido centralizado para a cena de fechamento.
    Os nós vão se acendendo de 1 a 8 na ordem da narração.
    """
    center_x = 960
    center_y = 520
    
    # Layout em elipse / teia elegante
    angles = [math.radians(a) for a in [225, 270, 315, 0, 45, 90, 135, 180]]
    rx, ry = 420, 220
    
    coords = []
    for a in angles:
        cx = int(center_x + rx * math.cos(a))
        cy = int(center_y + ry * math.sin(a))
        coords.append((cx, cy))
        
    font_node = get_font(22)
    
    # Linhas de interconexão
    for i in range(min(lighted_count, len(NODES_ORDER)) - 1):
        p1 = coords[i]
        p2 = coords[i+1]
        draw.line([p1, p2], fill=COLOR_ACCENT, width=4)
        
    # Conexões estruturais extras com o centro
    for i in range(min(lighted_count, len(NODES_ORDER))):
        p = coords[i]
        draw.line([center_x, center_y, p[0], p[1]], fill=(60, 85, 125), width=2)

    # Desenha o núcleo central
    draw.ellipse([center_x - 30, center_y - 30, center_x + 30, center_y + 30], fill=COLOR_ACCENT, outline=(255, 255, 255), width=3)
    
    # Desenha cada nó
    for i, name in enumerate(NODES_ORDER):
        cx, cy = coords[i]
        is_lit = (i < lighted_count)
        
        fill_col = COLOR_ACCENT if is_lit else (40, 60, 95)
        border_col = (255, 255, 255) if is_lit else (80, 100, 135)
        r = 22 if is_lit else 16
        
        draw.ellipse([cx - r, cy - r, cx + r, cy + r], fill=fill_col, outline=border_col, width=3)
        
        label = name.upper()
        bbox = font_node.getbbox(label)
        tw = bbox[2] - bbox[0]
        th = bbox[3] - bbox[1]
        
        offset_y = 30 if cy > center_y else -45
        draw.text((cx - tw // 2, cy + offset_y), label, fill=(255, 255, 255) if is_lit else (140, 160, 190), font=font_node)
        
    if show_question_node:
        # Novo nó vazio com ponto de interrogação ao lado de plasticidade (índice 4)
        px, py = coords[4]
        qx = px + 140
        qy = py - 40
        draw.line([px, py, qx, qy], fill=COLOR_ALERT, width=3)
        draw.ellipse([qx - 25, qy - 25, qx + 25, qy + 25], fill=COLOR_BG_DARK, outline=COLOR_ALERT, width=4)
        draw.text((qx - 8, qy - 18), "?", fill=COLOR_ALERT, font=get_font(32))
