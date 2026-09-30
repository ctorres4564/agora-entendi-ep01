import os
import json
import sys

# Adiciona raiz ao path para importar services e components
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from services.scene_renderer import render_scene_for_segment

def main():
    timeline_file = "assets/audio/timeline_cenas.json"
    if not os.path.exists(timeline_file):
        print(f"Erro: Arquivo {timeline_file} não encontrado. Execute generate_narration.py primeiro.")
        return
        
    with open(timeline_file, "r", encoding="utf-8") as f:
        data = json.load(f)
        
    timeline = data["timeline"]
    total = len(timeline)
    
    out_dir = "assets/images/scenes"
    os.makedirs(out_dir, exist_ok=True)
    
    print(f"Iniciando renderização de {total} cenas visuais sincronizadas (1920x1080)...")
    
    for idx, seg in enumerate(timeline):
        frame_path = os.path.join(out_dir, f"scene_{idx:03d}.png")
        img = render_scene_for_segment(seg, idx, total)
        img.save(frame_path, "PNG")
        if (idx + 1) % 10 == 0 or idx == total - 1:
            print(f"Renderizado: {idx + 1}/{total} quadros ({seg['block_title']})")
            
    print(f"\nTodas as {total} cenas foram renderizadas com sucesso em {out_dir}!")

if __name__ == "__main__":
    main()
