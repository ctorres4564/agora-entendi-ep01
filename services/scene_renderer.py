import os
import math
import json
from PIL import Image, ImageDraw, ImageFont
from components.episode_map import draw_mini_map, draw_center_map, NODES_ORDER
from components.typography import draw_on_screen_text, get_font

WIDTH = 1920
HEIGHT = 1080

COLOR_BG_LIGHT = (245, 241, 234) # #F5F1EA
COLOR_BG_DARK = (20, 33, 61)     # #14213D
COLOR_ACCENT = (242, 169, 0)     # #F2A900
COLOR_ALERT = (209, 73, 91)      # #D1495B
COLOR_TEXT_DARK = (26, 32, 44)
COLOR_TEXT_LIGHT = (245, 245, 245)

def create_base_canvas(is_dark=False):
    bg = COLOR_BG_DARK if is_dark else COLOR_BG_LIGHT
    img = Image.new("RGBA", (WIDTH, HEIGHT), bg)
    return img, ImageDraw.Draw(img)

def render_scene_for_segment(seg, seg_idx, total_segs):
    """
    Renderiza um frame mestre representativo em 1920x1080 para cada segmento da timeline.
    """
    block_id = seg["block_id"]
    p_idx = seg["paragraph_idx"]
    text = seg["text"]
    on_screen_text = seg["on_screen_text"]
    active_node = seg["node"]
    
    is_dark = (block_id in ["conceito_4", "fechamento"]) or ("noite" in text.lower()) or ("sono" in text.lower() and p_idx in [0, 1, 2, 3])
    img, draw = create_base_canvas(is_dark=is_dark)
    
    # 1. Renderiza o mapa do episódio no canto superior direito (exceto fechamento)
    if block_id != "fechamento":
        draw_mini_map(draw, active_node, is_dark_bg=is_dark)
        
    # 2. Desenha o visual específico da cena
    if block_id == "abertura":
        # Celular + chocolate + dopamina + etiqueta prazer
        cx, cy = 960, 480
        # Mesa suave
        draw.rectangle([200, 720, 1720, 740], fill=(215, 210, 200))
        
        # Celular genérico (sem marcas)
        phone_w, phone_h = 240, 440
        phone_x, phone_y = cx - 360, cy - 180
        draw.rounded_rectangle([phone_x, phone_y, phone_x + phone_w, phone_y + phone_h], radius=24, fill=(35, 40, 50), outline=(150, 155, 165), width=4)
        draw.rounded_rectangle([phone_x + 12, phone_y + 16, phone_x + phone_w - 12, phone_y + phone_h - 16], radius=16, fill=(240, 243, 246))
        # Notificação de curtida no celular
        draw.rounded_rectangle([phone_x + 25, phone_y + 60, phone_x + phone_w - 25, phone_y + 140], radius=12, fill=(255, 255, 255), outline=(220, 225, 230), width=2)
        draw.ellipse([phone_x + 40, phone_y + 82, phone_x + 75, phone_y + 117], fill=COLOR_ALERT)
        draw.text((phone_x + 90, phone_y + 88), "NOVA CURTIDA", fill=COLOR_TEXT_DARK, font=get_font(16))
        
        # Chocolate mordido ao lado
        choc_x, choc_y = cx - 40, cy + 20
        draw.rectangle([choc_x, choc_y, choc_x + 180, choc_y + 120], fill=(92, 54, 38))
        draw.rectangle([choc_x + 10, choc_y + 10, choc_x + 85, choc_y + 55], fill=(75, 42, 28))
        draw.rectangle([choc_x + 95, choc_y + 10, choc_x + 170, choc_y + 55], fill=(75, 42, 28))
        draw.rectangle([choc_x + 10, choc_y + 65, choc_x + 85, choc_y + 110], fill=(75, 42, 28))
        # Mordida
        draw.ellipse([choc_x + 140, choc_y - 20, choc_x + 200, choc_y + 40], fill=COLOR_BG_LIGHT)
        
        # Molécula estilizada de dopamina
        mol_x, mol_y = cx + 380, cy - 60
        hex_points = []
        for a in range(6):
            ang = math.radians(60 * a - 30)
            hex_points.append((mol_x + 70 * math.cos(ang), mol_y + 70 * math.sin(ang)))
        draw.polygon(hex_points, outline=(40, 60, 95), fill=None, width=4)
        for pt in hex_points:
            draw.ellipse([pt[0] - 8, pt[1] - 8, pt[0] + 8, pt[1] + 8], fill=COLOR_ACCENT)
        # Ramo da molécula
        draw.line([hex_points[1], (mol_x + 120, mol_y - 80)], fill=(40, 60, 95), width=4)
        draw.line([(mol_x + 120, mol_y - 80), (mol_x + 180, mol_y - 70)], fill=(40, 60, 95), width=4)
        draw.text((mol_x + 195, mol_y - 85), "NH2", fill=(40, 60, 95), font=get_font(20))
        
        # Etiqueta PRAZER presa na molécula
        has_question = ("não é exatamente assim" in text.lower()) or (p_idx >= 3)
        tag_w, tag_h = 240, 64
        tx, ty = mol_x - 30, mol_y + 100
        draw.line([mol_x, mol_y + 35, tx + 20, ty], fill=(150, 150, 150), width=2)
        draw.rectangle([tx, ty, tx + tag_w, ty + tag_h], fill=(255, 255, 255), outline=(180, 180, 180), width=2)
        tag_label = "PRAZER?" if has_question else "PRAZER"
        draw.text((tx + 40, ty + 12), tag_label, fill=COLOR_ALERT if has_question else COLOR_TEXT_DARK, font=get_font(32))
        
        if p_idx >= 4:
            # Zoom na célula / neurônio único no centro
            draw.rectangle([0, 0, WIDTH, HEIGHT], fill=COLOR_BG_LIGHT)
            draw_mini_map(draw, active_node, is_dark_bg=False)
            # Neurônio central único
            draw_neuron(draw, 960, 500, scale=1.5, pulse=True)
            draw.text((880, 360), "UMA ÚNICA CÉLULA: O NEURÔNIO", fill=COLOR_TEXT_DARK, font=get_font(22))
            
    elif block_id == "conceito_1":
        # Neurônio: corpo celular, dendritos (recebe), axônio longo (envia), panela quente, 86 bilhões
        if p_idx in [0, 1, 2, 3]:
            # Diagrama anatômico do neurônio
            draw_neuron(draw, 900, 500, scale=1.3, pulse=True, show_labels=True)
        elif p_idx in [4, 5]:
            # Panela quente e arco reflexo
            draw_hot_pan_scene(draw)
        elif p_idx in [6, 7, 8, 9]:
            # Contagem dos 86 bilhões e Suzana Herculano-Houzel
            draw_counting_scene(draw, text)
        else:
            # Transição: neurônio se preparando para o próximo
            draw_neuron(draw, 700, 500, scale=1.0, pulse=False)
            draw_neuron(draw, 1250, 500, scale=1.0, pulse=True)
            draw.line([(950, 500), (1050, 500)], fill=COLOR_ACCENT, width=3)
            
    elif block_id == "conceito_2":
        # Sinapse: fila de pessoas cochichando -> viram neurônios -> mito do fio emendado -> fenda sináptica
        if p_idx in [0, 1]:
            # Pessoas cochichando em fila
            draw_whisper_chain(draw)
        elif p_idx in [2, 3, 4]:
            # Mito dos fios elétricos emendados com fita isolante
            draw_wire_myth(draw)
        else:
            # Zoom no espaço sináptico (fenda)
            draw_synaptic_gap(draw, pulse_stopped=True)
            
    elif block_id == "conceito_3":
        # Neurotransmissor: química cruzando, chave e fechadura, dopamina, experimento de ratos
        if p_idx in [0, 1, 2, 3, 4]:
            # Vesículas e neurotransmissores atravessando a fenda e se ligando a receptores
            draw_synaptic_transmission(draw, highlight_dopamine=(p_idx >= 3))
        elif p_idx in [5, 6, 7, 8]:
            # Rato ilustrado no laboratório (sem fotos reais)
            draw_rat_experiment(draw, text)
        else:
            # Querer vs Gostar e Celular vibrando
            draw_wanting_vs_liking(draw)
            
    elif block_id == "conceito_4":
        # Redes cerebrais: Cidade à noite, bairros (visão, movimento, linguagem), mito dos 10%
        draw_brain_city_night(draw, text, p_idx)
        
    elif block_id == "conceito_5":
        # Plasticidade: Trilha no gramado -> conexões fortalecendo/enfraquecendo -> aprender a dirigir -> instrumento
        if p_idx in [0, 1]:
            draw_grass_trail(draw)
        elif p_idx in [2, 3, 4]:
            draw_synaptic_plasticity(draw)
        elif p_idx in [5, 6, 7, 8]:
            draw_driving_scene(draw, p_idx)
        else:
            draw_adult_music(draw)
            
    elif block_id == "conceito_6":
        # Memória: Pasta festa_2015 quebrando em peças e se reconstruindo, dois irmãos, Elizabeth Loftus
        if p_idx in [0, 1, 2, 3, 4]:
            draw_memory_reconstruction(draw)
        elif p_idx in [5, 6, 7]:
            draw_two_brothers_memory(draw)
        else:
            draw_loftus_experiment(draw)
            
    elif block_id == "conceito_7":
        # Atenção: Filtro/holofote no palco, festa barulhenta chamando nome, multitarefa alternando
        if p_idx in [0, 1, 2]:
            draw_sensory_filter_spotlight(draw)
        elif p_idx in [3, 4]:
            draw_party_cocktail_effect(draw)
        else:
            draw_multitasking_scene(draw)
            
    elif block_id == "conceito_8":
        # Sono: Interruptor apagando, cérebro não desliga, manutenção noturna das ruas, replay neural
        if p_idx in [0, 1, 2, 3, 4]:
            draw_sleep_replay_scene(draw)
        else:
            draw_sleep_consolidation_study(draw)
            
    elif block_id == "fechamento":
        # Fechamento: Mapa central se iluminando nó por nó -> pergunta final -> marca AGORA ENTENDI
        if p_idx <= 6:
            # 8 nós iluminando progressivamente
            lit_count = min(8, p_idx + 2)
            draw_center_map(draw, lighted_count=lit_count, show_question_node=False)
            draw_on_screen_text(draw, "MAPA BÁSICO DO CÉREBRO", y=900, is_dark_bg=True)
        elif p_idx in [7, 8]:
            # Pergunta no ar com nó ?
            draw_center_map(draw, lighted_count=8, show_question_node=True)
            draw_on_screen_text(draw, "COMO O CÉREBRO APRENDE?", y=900, is_dark_bg=True)
        else:
            # Cartela final com marca AGORA ENTENDI
            draw.rectangle([0, 0, WIDTH, HEIGHT], fill=COLOR_BG_DARK)
            font_logo = get_font(72)
            logo_text = "AGORA ENTENDI"
            bbox = font_logo.getbbox(logo_text)
            tw = bbox[2] - bbox[0]
            draw.text(((WIDTH - tw) // 2, 470), logo_text, fill=(255, 255, 255), font=font_logo)
            draw.text(((WIDTH - 380) // 2, 570), "ASSUNTOS DIFÍCEIS. EXPLICADOS DO COMEÇO.", fill=COLOR_ACCENT, font=get_font(20))
            return img

    # 3. Renderiza o texto obrigatório na tela (em caixa alta, geométrico, máx 5 palavras)
    if block_id != "fechamento":
        draw_on_screen_text(draw, on_screen_text, y=890, is_dark_bg=is_dark)

    return img

# --- Funções auxiliares de desenho visual pedagógico ---

def draw_neuron(draw, cx, cy, scale=1.0, pulse=False, show_labels=False):
    # Corpo celular (Soma)
    r = int(55 * scale)
    draw.ellipse([cx - r, cy - r, cx + r, cy + r], fill=(40, 60, 95), outline=(26, 32, 44), width=3)
    draw.ellipse([cx - r//2, cy - r//2, cx + r//2, cy + r//2], fill=(60, 85, 125)) # Núcleo
    
    # Ramificações dendríticas (Recebe)
    dendrites = [
        (-90, -60), (-120, -10), (-100, 50), (-80, 90), (-50, -100)
    ]
    for dx, dy in dendrites:
        end_x = int(cx + dx * scale)
        end_y = int(cy + dy * scale)
        draw.line([(cx - 30 * scale, cy), (end_x, end_y)], fill=(40, 60, 95), width=int(5 * scale))
        draw.line([(end_x, end_y), (end_x - 30, end_y - 20)], fill=(40, 60, 95), width=int(3 * scale))
        draw.line([(end_x, end_y), (end_x - 30, end_y + 20)], fill=(40, 60, 95), width=int(3 * scale))
        
    # Axônio longo (Envia)
    axon_len = int(480 * scale)
    axon_end_x = cx + axon_len
    draw.line([(cx + r, cy), (axon_end_x, cy)], fill=(40, 60, 95), width=int(8 * scale))
    
    # Bainhas de mielina
    num_sheaths = 4
    seg_w = int(75 * scale)
    gap = int(25 * scale)
    start_x = cx + r + 30
    for s in range(num_sheaths):
        sx = start_x + s * (seg_w + gap)
        draw.rounded_rectangle([sx, cy - int(18*scale), sx + seg_w, cy + int(18*scale)], radius=8, fill=(80, 110, 155), outline=(26, 32, 44), width=2)
        
    # Terminais axônicos
    terminals = [(axon_end_x + 50, cy - 40), (axon_end_x + 65, cy), (axon_end_x + 50, cy + 40)]
    for tx, ty in terminals:
        draw.line([(axon_end_x, cy), (tx, ty)], fill=(40, 60, 95), width=int(4 * scale))
        draw.ellipse([tx - 6, ty - 6, tx + 6, ty + 6], fill=COLOR_ACCENT)
        
    if pulse:
        # Pulso de luz amarelo-âmbar percorrendo o axônio
        px = start_x + int(160 * scale)
        draw.ellipse([px - 14, cy - 14, px + 14, cy + 14], fill=COLOR_ACCENT, outline=(255, 255, 255), width=3)
        draw.line([(px - 30, cy), (px + 30, cy)], fill=COLOR_ACCENT, width=6)
        
    if show_labels:
        font_lbl = get_font(20)
        # Rótulo RECEBE
        draw.rectangle([cx - int(240*scale), cy - 40, cx - int(120*scale), cy], fill=(225, 220, 210), outline=(150, 150, 150), width=2)
        draw.text((cx - int(225*scale), cy - 35), "RECEBE", fill=COLOR_TEXT_DARK, font=font_lbl)
        # Rótulo ENVIA
        draw.rectangle([cx + int(240*scale), cy - int(60*scale), cx + int(340*scale), cy - int(20*scale)], fill=(225, 220, 210), outline=(150, 150, 150), width=2)
        draw.text((cx + int(255*scale), cy - int(55*scale)), "ENVIA", fill=COLOR_TEXT_DARK, font=font_lbl)

def draw_hot_pan_scene(draw):
    cx, cy = 960, 480
    # Fogão e panela
    draw.rectangle([cx - 400, cy + 100, cx - 100, cy + 120], fill=(120, 125, 135))
    # Chama sutil
    draw.ellipse([cx - 300, cy + 70, cx - 200, cy + 105], fill=COLOR_ALERT)
    # Panela quente
    draw.rectangle([cx - 320, cy - 20, cx - 180, cy + 75], fill=(50, 55, 65))
    draw.rectangle([cx - 180, cy + 10, cx - 60, cy + 25], fill=(70, 75, 85)) # Cabo da panela
    
    # Mão recuando rapidamente
    hx, hy = cx + 80, cy - 30
    draw.rounded_rectangle([hx, hy, hx + 160, hy + 70], radius=16, fill=(230, 190, 165), outline=(180, 140, 115), width=3)
    # Linhas de movimento de recuo
    draw.line([hx + 180, hy + 20, hx + 230, hy + 20], fill=(160, 160, 160), width=3)
    draw.line([hx + 175, hy + 45, hx + 225, hy + 45], fill=(160, 160, 160), width=3)
    
    # Linha de pulsos subindo pelo braço em direção à medula/cérebro
    arm_pts = [(hx + 80, hy + 35), (hx + 280, hy - 40), (hx + 420, hy - 140), (hx + 500, hy - 240)]
    for i in range(len(arm_pts) - 1):
        draw.line([arm_pts[i], arm_pts[i+1]], fill=(180, 185, 195), width=4)
        # Pulsos de sinal elétrico ultra-rápido
        mid = ((arm_pts[i][0] + arm_pts[i+1][0])//2, (arm_pts[i][1] + arm_pts[i+1][1])//2)
        draw.ellipse([mid[0]-10, mid[1]-10, mid[0]+10, mid[1]+10], fill=COLOR_ACCENT)

def draw_counting_scene(draw, text):
    cx, cy = 960, 480
    font_large = get_font(72)
    font_author = get_font(30)
    
    # Livro didático antigo
    draw.rectangle([cx - 480, cy - 140, cx + 480, cy + 140], fill=(255, 255, 255), outline=(210, 205, 195), width=3)
    
    # 100 BILHÕES riscado
    draw.text((cx - 360, cy - 80), "100 BILHÕES", fill=(140, 145, 155), font=font_large)
    draw.line([cx - 380, cy - 40, cx + 220, cy - 40], fill=COLOR_ALERT, width=8)
    
    # 86 BILHÕES em destaque
    draw.text((cx - 360, cy + 10), "86 BILHÕES", fill=COLOR_ACCENT, font=font_large)
    
    # Apenas o nome da cientista em texto (SEM ROSTO, SEM FOTO)
    draw.rectangle([cx - 360, cy + 180, cx + 360, cy + 240], fill=(235, 230, 220))
    draw.text((cx - 330, cy + 195), "SUZANA HERCULANO-HOUZEL (UFRJ)", fill=COLOR_TEXT_DARK, font=font_author)

def draw_whisper_chain(draw):
    cx, cy = 960, 480
    spacing = 260
    start_x = 420
    for i in range(4):
        px = start_x + i * spacing
        # Cabeça / silhueta amigável
        draw.ellipse([px - 45, cy - 100, px + 45, cy - 10], fill=(60, 85, 125))
        draw.rounded_rectangle([px - 60, cy, px + 60, cy + 140], radius=20, fill=(80, 110, 155))
        # Balão de fala cochicho
        if i < 3:
            draw.line([px + 35, cy - 50, px + spacing - 40, cy - 50], fill=COLOR_ACCENT, width=3)
            draw.ellipse([px + spacing - 45, cy - 54, px + spacing - 37, cy - 46], fill=COLOR_ACCENT)

def draw_wire_myth(draw):
    cx, cy = 960, 480
    # Dois fios de cobre se encontrando
    draw.line([cx - 450, cy, cx - 40, cy], fill=(184, 115, 51), width=18)
    draw.line([cx + 40, cy, cx + 450, cy], fill=(184, 115, 51), width=18)
    # Fita isolante preta desfeita
    draw.rectangle([cx - 70, cy - 25, cx + 70, cy + 25], fill=(30, 30, 30), outline=COLOR_ALERT, width=3)
    draw.line([cx - 90, cy - 40, cx + 90, cy + 40], fill=COLOR_ALERT, width=6)
    draw.text((cx - 210, cy - 140), "MITO: FIOS EMENDADOS", fill=COLOR_ALERT, font=get_font(28))

def draw_synaptic_gap(draw, pulse_stopped=True):
    cx, cy = 960, 460
    # Terminal pré-sináptico (esquerda)
    draw.ellipse([cx - 600, cy - 260, cx - 60, cy + 260], fill=(40, 60, 95))
    # Terminal pós-sináptico (direita)
    draw.ellipse([cx + 60, cy - 260, cx + 600, cy + 260], fill=(40, 60, 95))
    
    # Fenda sináptica no meio (espaço vazio destacado)
    draw.line([cx - 60, cy - 220, cx - 60, cy + 220], fill=COLOR_ACCENT, width=4)
    draw.line([cx + 60, cy - 220, cx + 60, cy + 220], fill=(120, 140, 175), width=4)
    
    # Cota do espaço minúsculo
    draw.line([cx - 50, cy - 280, cx + 50, cy - 280], fill=COLOR_TEXT_DARK, width=2)
    draw.text((cx - 140, cy - 330), "ESPAÇO MINÚSCULO: SINAPSE", fill=COLOR_TEXT_DARK, font=get_font(20))
    
    if pulse_stopped:
        # Pulso elétrico chega na ponta e para (piscando)
        draw.ellipse([cx - 95, cy - 25, cx - 45, cy + 25], fill=COLOR_ACCENT, outline=(255, 255, 255), width=4)
        draw.text((cx - 130, cy + 50), "O SINAL PARA AQUI", fill=COLOR_ALERT, font=get_font(20))

def draw_synaptic_transmission(draw, highlight_dopamine=False):
    cx, cy = 960, 460
    draw.ellipse([cx - 600, cy - 260, cx - 60, cy + 260], fill=(40, 60, 95))
    draw.ellipse([cx + 60, cy - 260, cx + 600, cy + 260], fill=(50, 75, 115))
    
    # Vesículas / Esferas químicas cruzando o espaço
    import random
    random.seed(42)
    for i in range(16):
        bx = cx - 50 + (i % 4) * 30
        by = cy - 160 + (i * 22)
        col = (80, 190, 220)
        draw.ellipse([bx - 10, by - 10, bx + 10, by + 10], fill=col, outline=(255, 255, 255), width=2)
        
    if highlight_dopamine:
        # Esfera de dopamina em amarelo-âmbar com rótulo
        dop_x, dop_y = cx - 5, cy - 20
        draw.ellipse([dop_x - 18, dop_y - 18, dop_x + 18, dop_y + 18], fill=COLOR_ACCENT, outline=(255, 255, 255), width=4)
        draw.rectangle([dop_x - 80, dop_y - 70, dop_x + 80, dop_y - 30], fill=COLOR_ACCENT)
        draw.text((dop_x - 65, dop_y - 62), "DOPAMINA", fill=COLOR_TEXT_DARK, font=get_font(22))
        
    # Receptores ("fechaduras") no neurônio pós-sináptico
    for ry in range(cy - 160, cy + 180, 50):
        draw.arc([cx + 50, ry - 14, cx + 78, ry + 14], 90, 270, fill=COLOR_ACCENT, width=5)

def draw_rat_experiment(draw, text):
    cx, cy = 960, 480
    # Laboratório ilustrado 2D flat estilizado (sem experimentos reais)
    # Mesa de laboratório
    draw.rectangle([300, 680, 1620, 710], fill=(200, 205, 215))
    
    # Rato ilustrado estilizado (formas geométricas suaves, amigável)
    rx, ry = cx - 80, cy + 100
    # Corpo
    draw.ellipse([rx - 90, ry - 60, rx + 70, ry + 40], fill=(160, 165, 175), outline=(120, 125, 135), width=3)
    # Cabeça
    draw.polygon([(rx + 50, ry - 30), (rx + 150, ry), (rx + 50, ry + 20)], fill=(160, 165, 175))
    # Olho expressivo
    draw.ellipse([rx + 85, ry - 12, rx + 97, ry], fill=(40, 40, 40))
    # Focinho / lambendo os lábios
    draw.ellipse([rx + 145, ry - 4, rx + 155, ry + 6], fill=COLOR_ALERT)
    # Orelha
    draw.ellipse([rx + 35, ry - 55, rx + 75, ry - 15], fill=(225, 175, 175))
    # Rabo ondulado
    draw.arc([rx - 160, ry - 40, rx - 80, ry + 40], 0, 180, fill=(160, 165, 175), width=5)
    
    # Pote de comida ao lado
    px, py = cx + 240, cy + 110
    draw.rectangle([px, py, px + 100, py + 50], fill=(180, 120, 70))
    draw.text((px + 10, py + 12), "COMIDA", fill=(255, 255, 255), font=get_font(18))
    
    # Texto na tela com o nome do pesquisador
    draw.rectangle([cx - 260, cy - 220, cx + 260, cy - 160], fill=(235, 230, 220))
    draw.text((cx - 230, cy - 205), "KENT BERRIDGE (ANOS 1980)", fill=COLOR_TEXT_DARK, font=get_font(24))

def draw_wanting_vs_liking(draw):
    cx, cy = 960, 480
    # Contraste: QUERER vs GOSTAR
    box_w = 400
    box_h = 240
    
    # Caixa QUERER
    draw.rectangle([cx - 460, cy - 120, cx - 60, cy + 120], fill=(255, 255, 255), outline=COLOR_ACCENT, width=4)
    draw.text((cx - 360, cy - 70), "QUERER", fill=COLOR_ACCENT, font=get_font(44))
    draw.text((cx - 430, cy + 10), "MOTIVAÇÃO / BUSCA", fill=COLOR_TEXT_DARK, font=get_font(22))
    draw.text((cx - 430, cy + 45), "(DOPAMINA)", fill=(120, 120, 120), font=get_font(20))
    
    # Caixa GOSTAR
    draw.rectangle([cx + 60, cy - 120, cx + 460, cy + 120], fill=(255, 255, 255), outline=(140, 150, 165), width=3)
    draw.text((cx + 170, cy - 70), "GOSTAR", fill=(80, 95, 120), font=get_font(44))
    draw.text((cx + 120, cy + 10), "PRAZER DO CONSUMO", fill=COLOR_TEXT_DARK, font=get_font(22))
    draw.text((cx + 120, cy + 45), "(OUTROS CIRCUITOS)", fill=(120, 120, 120), font=get_font(20))

def draw_brain_city_night(draw, text, p_idx):
    cx, cy = 960, 480
    # Cidade cerebral à noite (#14213D)
    # Bairros conectados por avenidas de luz
    districts = [
        {"name": "VISÃO", "pos": (cx - 280, cy - 120), "lit": True},
        {"name": "AUDIÇÃO", "pos": (cx - 140, cy + 100), "lit": True},
        {"name": "MEMÓRIA", "pos": (cx + 80, cy - 80), "lit": True},
        {"name": "EMOÇÃO", "pos": (cx + 220, cy + 80), "lit": True},
        {"name": "LINGUAGEM", "pos": (cx - 40, cy - 220), "lit": (p_idx >= 2)},
        {"name": "MOVIMENTO", "pos": (cx + 280, cy - 160), "lit": (p_idx >= 4)}
    ]
    
    # Avenidas de luz entre bairros
    for i in range(len(districts)):
        for j in range(i+1, len(districts)):
            d1, d2 = districts[i], districts[j]
            is_lit_path = d1["lit"] and d2["lit"]
            col = COLOR_ACCENT if is_lit_path else (45, 65, 95)
            w = 4 if is_lit_path else 2
            draw.line([d1["pos"], d2["pos"]], fill=col, width=w)
            
    # Bairros (clusters de luz)
    for d in districts:
        bx, by = d["pos"]
        r = 50
        col = COLOR_ACCENT if d["lit"] else (35, 50, 75)
        border = (255, 255, 255) if d["lit"] else (60, 80, 110)
        draw.ellipse([bx - r, by - r, bx + r, by + r], fill=col, outline=border, width=3)
        draw.text((bx - 40, by - 10), d["name"], fill=(20, 33, 61) if d["lit"] else (160, 180, 205), font=get_font(18))
        
    if "10%" in text or p_idx in [6, 7, 8, 9, 10]:
        # Caixa de mito dos 10% riscada
        draw.rectangle([cx - 200, cy + 180, cx + 200, cy + 280], fill=(20, 33, 61, 230), outline=COLOR_ALERT, width=3)
        draw.text((cx - 100, cy + 195), "10%?", fill=(255, 255, 255), font=get_font(52))
        draw.line([cx - 140, cy + 235, cx + 140, cy + 235], fill=COLOR_ALERT, width=8)

def draw_grass_trail(draw):
    cx, cy = 960, 480
    # Gramado verde suave
    draw.rectangle([200, 200, 1720, 800], fill=(185, 205, 170))
    # Trilha marcada pelo uso (terra batida)
    trail_pts = [(300, 680), (600, 520), (960, 460), (1350, 420), (1650, 350)]
    for i in range(len(trail_pts) - 1):
        draw.line([trail_pts[i], trail_pts[i+1]], fill=(195, 165, 125), width=45)
    # Trilha antiga abandonada sendo coberta pelo mato
    old_pts = [(600, 520), (800, 680), (1100, 720)]
    for i in range(len(old_pts) - 1):
        draw.line([old_pts[i], old_pts[i+1]], fill=(180, 195, 160), width=18)
    draw.text((640, 380), "CAMINHO REFORÇADO PELO USO", fill=(50, 70, 40), font=get_font(24))

def draw_synaptic_plasticity(draw):
    cx, cy = 960, 480
    # Conexão fortalecida (espessa e dourada)
    draw.text((cx - 420, cy - 160), "MUITO USADA: FORTALECE", fill=COLOR_ACCENT, font=get_font(24))
    draw.line([cx - 450, cy - 80, cx - 100, cy - 80], fill=COLOR_ACCENT, width=16)
    draw.ellipse([cx - 470, cy - 100, cx - 430, cy - 60], fill=(40, 60, 95))
    draw.ellipse([cx - 120, cy - 100, cx - 80, cy - 60], fill=(40, 60, 95))
    
    # Conexão enfraquecida (fina e apagada)
    draw.text((cx + 100, cy - 160), "SEM USO: ENFRAQUECE", fill=(140, 150, 165), font=get_font(24))
    draw.line([cx + 100, cy - 80, cx + 450, cy - 80], fill=(180, 185, 195), width=3)
    draw.ellipse([cx + 80, cy - 100, cx + 120, cy - 60], fill=(120, 130, 145))
    draw.ellipse([cx + 430, cy - 100, cx + 470, cy - 60], fill=(120, 130, 145))

def draw_driving_scene(draw, p_idx):
    cx, cy = 960, 480
    # Volante e painel de direção
    draw.ellipse([cx - 140, cy - 120, cx + 140, cy + 160], outline=(40, 45, 55), width=24)
    draw.line([cx - 130, cy + 20, cx + 130, cy + 20], fill=(40, 45, 55), width=18)
    draw.line([cx, cy + 20, cx, cy + 150], fill=(40, 45, 55), width=18)
    if p_idx in [5, 6]:
        # Aprendiz tenso: alerta
        draw.text((cx - 260, cy - 220), "PRIMEIRAS AULAS: ATENÇÃO TOTAL", fill=COLOR_ALERT, font=get_font(28))
    else:
        # Meses depois: automático
        draw.text((cx - 260, cy - 220), "CONEXÕES AUTOMATIZADAS", fill=COLOR_ACCENT, font=get_font(28))

def draw_adult_music(draw):
    cx, cy = 960, 480
    # Violão e notas musicais
    draw.text((cx - 320, cy - 180), "PLASTICIDADE PELA VIDA TODA", fill=COLOR_TEXT_DARK, font=get_font(32))
    # Violão estilizado 2D
    draw.ellipse([cx - 120, cy - 40, cx + 120, cy + 180], fill=(190, 130, 75))
    draw.ellipse([cx - 40, cy + 30, cx + 40, cy + 110], fill=(40, 40, 40)) # Boca do violão
    draw.line([cx, cy - 40, cx, cy - 240], fill=(140, 90, 50), width=22) # Braço
    # Cordas
    for off in [-6, -2, 2, 6]:
        draw.line([cx + off, cy - 240, cx + off, cy + 140], fill=(230, 230, 230), width=2)

def draw_memory_reconstruction(draw):
    cx, cy = 960, 480
    # Pasta festa_2015 se abrindo e quebrando em peças flutuantes
    draw.rectangle([cx - 160, cy - 220, cx + 160, cy - 150], fill=(240, 190, 80))
    draw.text((cx - 100, cy - 195), "festa_2015", fill=(40, 40, 40), font=get_font(20))
    
    # Fragmentos reconstruídos
    fragments = [
        ("BOLO", (cx - 340, cy - 40), COLOR_ACCENT),
        ("BALÃO", (cx - 140, cy + 60), (220, 100, 120)),
        ("MÚSICA", (cx + 120, cy - 20), (80, 140, 210)),
        ("NOVO DETALHE (+)", (cx + 280, cy + 80), COLOR_ALERT)
    ]
    for label, pos, col in fragments:
        fx, fy = pos
        draw.rounded_rectangle([fx, fy, fx + 180, fy + 70], radius=12, fill=(255, 255, 255), outline=col, width=3)
        draw.text((fx + 20, fy + 22), label, fill=col, font=get_font(18))
        draw.line([cx, cy - 140, fx + 90, fy], fill=(200, 205, 215), width=2)

def draw_two_brothers_memory(draw):
    cx, cy = 960, 480
    # Dois irmãos com balões de pensamento diferentes sobre a mesma festa
    # Irmão 1
    draw.ellipse([cx - 420, cy + 40, cx - 320, cy + 140], fill=(60, 85, 125))
    draw.rectangle([cx - 490, cy - 160, cx - 250, cy - 20], fill=(255, 255, 255), outline=COLOR_ACCENT, width=3)
    draw.text((cx - 470, cy - 110), "VERSÃO A: 'CHOVEU'", fill=COLOR_TEXT_DARK, font=get_font(20))
    
    # Irmão 2
    draw.ellipse([cx + 320, cy + 40, cx + 420, cy + 140], fill=(80, 110, 155))
    draw.rectangle([cx + 250, cy - 160, cx + 490, cy - 20], fill=(255, 255, 255), outline=COLOR_ALERT, width=3)
    draw.text((cx + 270, cy - 110), "VERSÃO B: 'FEZ SOL'", fill=COLOR_TEXT_DARK, font=get_font(20))

def draw_loftus_experiment(draw):
    cx, cy = 960, 480
    draw.rectangle([cx - 360, cy - 120, cx + 360, cy + 120], fill=(255, 255, 255), outline=(200, 205, 215), width=3)
    draw.text((cx - 260, cy - 70), "ELIZABETH LOFTUS", fill=COLOR_TEXT_DARK, font=get_font(38))
    draw.text((cx - 310, cy + 20), "EXPERIMENTOS DE MEMÓRIA E SUGESTÃO", fill=COLOR_ACCENT, font=get_font(22))

def draw_sensory_filter_spotlight(draw):
    cx, cy = 960, 480
    # Chuva de ícones sensoriais convergindo
    draw.ellipse([cx - 80, cy - 80, cx + 80, cy + 80], fill=(40, 60, 95))
    # Cone de holofote âmbar
    draw.polygon([(cx, cy - 280), (cx - 180, cy + 180), (cx + 180, cy + 180)], fill=(242, 169, 0, 70))
    draw.text((cx - 110, cy + 210), "HOLOFOTE DA ATENÇÃO", fill=COLOR_ACCENT, font=get_font(22))

def draw_party_cocktail_effect(draw):
    cx, cy = 960, 480
    # Festa: balões com barulho e um balão distante "...CLAUDIA..."
    draw.text((cx - 380, cy - 120), "BARULHO...", fill=(180, 185, 195), font=get_font(28))
    draw.text((cx + 180, cy + 40), "CONVERSAS...", fill=(180, 185, 195), font=get_font(28))
    # Balão em destaque sob o holofote
    draw.rectangle([cx - 160, cy - 40, cx + 160, cy + 40], fill=COLOR_ACCENT)
    draw.text((cx - 95, cy - 15), "...CLAUDIA...", fill=(20, 33, 61), font=get_font(30))

def draw_multitasking_scene(draw):
    cx, cy = 960, 480
    # Tela dividida: Celular vs Caderno de estudo
    draw.rectangle([cx - 440, cy - 120, cx - 80, cy + 160], fill=(255, 255, 255), outline=(180, 180, 180), width=3)
    draw.text((cx - 330, cy - 70), "CELULAR", fill=COLOR_TEXT_DARK, font=get_font(24))
    
    draw.rectangle([cx + 80, cy - 120, cx + 440, cy + 160], fill=(255, 255, 255), outline=(180, 180, 180), width=3)
    draw.text((cx + 210, cy - 70), "AULA", fill=COLOR_TEXT_DARK, font=get_font(24))
    
    # Seta de alternância e relógio de custo de troca
    draw.line([cx - 60, cy + 20, cx + 60, cy + 20], fill=COLOR_ALERT, width=6)
    draw.text((cx - 120, cy + 80), "CUSTO DE TROCA", fill=COLOR_ALERT, font=get_font(22))

def draw_sleep_replay_scene(draw):
    cx, cy = 960, 480
    # Interruptor e cérebro que não desliga (replay neural acelerado)
    draw.text((cx - 380, cy - 180), "REPLAY NEURAL DURANTE O SONO", fill=COLOR_ACCENT, font=get_font(32))
    # Sequência de disparos em ratos e humanos
    for i in range(5):
        sx = cx - 320 + i * 160
        draw.ellipse([sx - 25, cy - 25, sx + 25, cy + 25], fill=COLOR_ACCENT, outline=(255, 255, 255), width=3)
        if i < 4:
            draw.line([sx + 25, cy, sx + 135, cy], fill=COLOR_ACCENT, width=4)

def draw_sleep_consolidation_study(draw):
    cx, cy = 960, 480
    draw.rectangle([cx - 360, cy - 100, cx + 360, cy + 100], fill=(255, 255, 255), outline=COLOR_ACCENT, width=3)
    draw.text((cx - 240, cy - 50), "CONSOLIDAÇÃO DA MEMÓRIA", fill=COLOR_TEXT_DARK, font=get_font(32))
    draw.text((cx - 280, cy + 20), "ESTUDAR DE DIA + DORMIR BEM = FIXAÇÃO", fill=COLOR_ACCENT, font=get_font(20))
