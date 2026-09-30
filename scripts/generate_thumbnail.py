from PIL import Image, ImageDraw, ImageFont
import math
import os

FONT_PATH = "assets/fonts/Montserrat.ttf"

def get_font(size):
    try:
        return ImageFont.truetype(FONT_PATH, size)
    except:
        return ImageFont.load_default()

def generate_thumbnail():
    width = 1280
    height = 720
    
    # Fundo off-white oficial (#F5F1EA)
    bg_color = (245, 241, 234)
    img = Image.new("RGBA", (width, height), bg_color)
    draw = ImageDraw.Draw(img)
    
    # Cores
    color_brain = (40, 60, 95)
    color_brain_glow = (242, 169, 0)
    color_alert = (209, 73, 91)
    color_text = (20, 33, 61)
    
    # 1. Desenho estilizado do Cérebro (2D Flat geométrico com conexões e hemisférios)
    brain_center_x = 420
    brain_center_y = 380
    
    # Círculos e curvas estilizadas representando os lobos e circunvoluções
    lobes = [
        # (x_offset, y_offset, radius)
        (-140, -40, 110),
        (-60, -110, 100),
        (50, -110, 95),
        (130, -50, 105),
        (140, 50, 100),
        (70, 110, 90),
        (-30, 120, 85),
        (-120, 70, 95),
        (0, 0, 130)
    ]
    
    # Silhueta de preenchimento suave
    for ox, oy, r in lobes:
        draw.ellipse([
            brain_center_x + ox - r, brain_center_y + oy - r,
            brain_center_x + ox + r, brain_center_y + oy + r
        ], fill=(228, 222, 212))
        
    # Conexões sinápticas brilhantes dentro do cérebro
    node_coords = [
        (brain_center_x - 110, brain_center_y - 30),
        (brain_center_x - 50, brain_center_y - 80),
        (brain_center_x + 40, brain_center_y - 70),
        (brain_center_x + 100, brain_center_y - 20),
        (brain_center_x + 90, brain_center_y + 60),
        (brain_center_x + 30, brain_center_y + 90),
        (brain_center_x - 40, brain_center_y + 80),
        (brain_center_x - 90, brain_center_y + 40),
        (brain_center_x, brain_center_y)
    ]
    
    for i in range(len(node_coords)):
        for j in range(i+1, len(node_coords)):
            dist = math.hypot(node_coords[i][0] - node_coords[j][0], node_coords[i][1] - node_coords[j][1])
            if dist < 140:
                draw.line([node_coords[i], node_coords[j]], fill=(195, 185, 170), width=3)
                
    # Linha de pulso em amarelo-âmbar
    draw.line([node_coords[0], node_coords[8]], fill=color_brain_glow, width=5)
    draw.line([node_coords[8], node_coords[3]], fill=color_brain_glow, width=5)
    
    # Nós do cérebro
    for pt in node_coords:
        draw.ellipse([pt[0] - 8, pt[1] - 8, pt[0] + 8, pt[1] + 8], fill=color_brain, outline=(255, 255, 255), width=2)
    draw.ellipse([node_coords[8][0] - 14, node_coords[8][1] - 14, node_coords[8][0] + 14, node_coords[8][1] + 14], fill=color_brain_glow, outline=color_brain, width=3)

    # 2. Etiqueta "PRAZER" com alfinete e riscada em vermelho
    tag_x = brain_center_x + 130
    tag_y = brain_center_y - 120
    tag_w = 260
    tag_h = 75
    
    # Linha ligando o cérebro à etiqueta
    draw.line([brain_center_x + 40, brain_center_y - 70, tag_x, tag_y + 35], fill=color_alert, width=3)
    
    # Card da etiqueta branca
    draw.rectangle([tag_x, tag_y, tag_x + tag_w, tag_y + tag_h], fill=(255, 255, 255), outline=(180, 180, 180), width=2)
    # Furo da etiqueta
    draw.ellipse([tag_x + 15, tag_y + 28, tag_x + 30, tag_y + 43], fill=bg_color, outline=(180, 180, 180), width=2)
    
    font_tag = get_font(38)
    draw.text((tag_x + 55, tag_y + 15), "PRAZER", fill=(80, 80, 80), font=font_tag)
    # Risco duplo em vermelho suave sobre "PRAZER"
    draw.line([tag_x + 40, tag_y + 55, tag_x + tag_w - 20, tag_y + 20], fill=color_alert, width=7)
    draw.line([tag_x + 40, tag_y + 20, tag_x + tag_w - 20, tag_y + 55], fill=color_alert, width=7)

    # 3. Tipografia Principal Grande: "NÃO É PRAZER"
    # Lado direito ou centralizado superior
    title_x = 760
    title_y = 230
    
    font_badge = get_font(28)
    # Badge do canal
    draw.rectangle([title_x, 140, title_x + 310, 185], fill=color_text)
    draw.text((title_x + 18, 146), "AGORA ENTENDI #1", fill=(255, 255, 255), font=font_badge)
    
    font_big = get_font(84)
    # Palavra "NÃO É"
    draw.text((title_x, 220), "NÃO É", fill=color_text, font=font_big)
    
    # Palavra "PRAZER" em caixa de destaque vermelho/alerta
    draw.rectangle([title_x, 340, title_x + 460, 470], fill=color_alert)
    draw.text((title_x + 22, 350), "PRAZER", fill=(255, 255, 255), font=font_big)
    
    # Subtítulo explicativo
    font_sub = get_font(32)
    draw.text((title_x, 505), "A VERDADE SOBRE A", fill=(90, 100, 115), font=font_sub)
    draw.text((title_x, 550), "DOPAMINA E O CÉREBRO", fill=color_brain_glow, font=font_sub)

    # 4. Salvar arquivos
    os.makedirs("assets/thumbnails", exist_ok=True)
    os.makedirs("output", exist_ok=True)
    
    out_asset = "assets/thumbnails/thumbnail_1280x720.png"
    out_final = "output/thumbnail_1280x720.png"
    img.save(out_asset, "PNG")
    img.save(out_final, "PNG")
    print(f"Thumbnail gerada com sucesso em:\n- {out_asset}\n- {out_final}")

if __name__ == "__main__":
    generate_thumbnail()
