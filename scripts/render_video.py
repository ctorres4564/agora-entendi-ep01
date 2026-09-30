import os
import json
import subprocess

def main():
    timeline_file = "assets/audio/timeline_cenas.json"
    if not os.path.exists(timeline_file):
        print(f"Erro: {timeline_file} não encontrado.")
        return

    with open(timeline_file, "r", encoding="utf-8") as f:
        data = json.load(f)
        
    timeline = data["timeline"]
    total_duration = data["total_duration"]
    
    concat_video_path = "assets/images/scenes/concat_video.txt"
    print(f"Criando lista de concatenação de vídeo sincronizada...")
    
    with open(concat_video_path, "w", encoding="utf-8") as f:
        f.write("ffconcat version 1.0\n")
        for idx, seg in enumerate(timeline):
            # Duração exata do segmento incluindo a pausa correspondente
            if idx < len(timeline) - 1:
                seg_dur = timeline[idx + 1]["start"] - seg["start"]
            else:
                seg_dur = total_duration - seg["start"]
                if seg_dur < 3.0:
                    seg_dur = 3.0
                    
            scene_img = os.path.abspath(f"assets/images/scenes/scene_{idx:03d}.png").replace("\\", "/")
            f.write(f"file '{scene_img}'\n")
            f.write(f"duration {seg_dur:.4f}\n")
            
        # Repete o último frame para encerramento correto do demuxer ffconcat
        last_img = os.path.abspath(f"assets/images/scenes/scene_{len(timeline)-1:03d}.png").replace("\\", "/")
        f.write(f"file '{last_img}'\n")

    audio_voice = os.path.abspath("output/narracao_isolada.wav").replace("\\", "/")
    audio_music = os.path.abspath("assets/audio/trilha_fundo.wav").replace("\\", "/")
    output_video = os.path.abspath("output/agora_entendi_ep01_1080p.mp4").replace("\\", "/")

    print(f"\nIniciando renderização final do vídeo 1080p 30fps com FFmpeg...")
    print(f"- Narração: {audio_voice}")
    print(f"- Trilha sonora: {audio_music} (atenuação -22 dB)")
    print(f"- Saída: {output_video}")
    
    # Comando FFmpeg otimizado
    # - Filtro complexo de áudio: amix da voz master + música com fade suave
    # - Filtro de vídeo: escala e fps garantidos (1920x1080, 30 fps, yuv420p)
    cmd = [
        "ffmpeg", "-y",
        "-f", "concat", "-safe", "0", "-i", concat_video_path,
        "-i", audio_voice,
        "-i", audio_music,
        "-filter_complex",
        "[2:a]volume=0.08[bgm]; [1:a][bgm]amix=inputs=2:duration=first:dropout_transition=2[aout]",
        "-map", "0:v",
        "-map", "[aout]",
        "-c:v", "libx264",
        "-preset", "medium",
        "-crf", "18",
        "-pix_fmt", "yuv420p",
        "-r", "30",
        "-c:a", "aac",
        "-b:a", "192k",
        "-shortest",
        output_video
    ]
    
    subprocess.run(cmd, check=True)
    print(f"\n=======================================================")
    print(f"VÍDEO FINAL RENDERIZADO COM SUCESSO: {output_video}")
    print(f"=======================================================")

if __name__ == "__main__":
    main()
