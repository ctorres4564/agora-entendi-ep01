import numpy as np
import subprocess
import os

def generate_calm_ambient_track(output_path="assets/audio/trilha_fundo.wav", duration=600.0, sample_rate=44100):
    print(f"Gerando trilha sonora instrumental ambiente suave ({duration:.1f} s)...")
    
    t = np.linspace(0, duration, int(sample_rate * duration), endpoint=False)
    
    # Progressão harmônica calma: Cmaj7 -> Am9 -> Fmaj7 -> Gsus4 (acordes lentos a cada 8 segundos)
    # Frequências fundamentais e harmônicos quentes de piano Rhodes e Synth Pad
    chords = [
        # Cmaj7: C3, G3, B3, E4
        [130.81, 196.00, 246.94, 329.63],
        # Am9: A2, E3, G3, B3, C4
        [110.00, 164.81, 196.00, 246.94, 261.63],
        # Fmaj7: F2, C3, E3, A3
        [87.31, 130.81, 164.81, 220.00],
        # Gsus4 -> G: G2, D3, G3, C4, B3
        [98.00, 146.83, 196.00, 261.63, 246.94]
    ]
    
    chord_len = 8.0 # cada acorde dura 8 segundos
    total_audio = np.zeros_like(t)
    
    for i, chord in enumerate(chords):
        # Repete a cada ciclo de 32 segundos (4 acordes * 8s)
        cycle_len = 32.0
        
        # Cria envelope e harmônicos suaves para cada nota
        for note_f in chord:
            # Onda senoidal com leve 2º harmônico para calor acústico
            wave = 0.65 * np.sin(2 * np.pi * note_f * t) + 0.25 * np.sin(4 * np.pi * note_f * t) + 0.10 * np.sin(6 * np.pi * note_f * t)
            
            # Envelope de acorde suave (LFO lento)
            cycle_pos = (t % cycle_len)
            chord_start = i * chord_len
            chord_end = (i + 1) * chord_len
            
            # Máscara de tempo com ataque e fade suaves
            in_chord = np.maximum(0.0, np.sin(np.pi * np.clip((cycle_pos - chord_start) / chord_len, 0.0, 1.0)))
            total_audio += wave * (in_chord ** 1.5)
            
    # Pulso rítmico ultra suave (sub-grave e marimba suave a cada 2 segundos)
    rhythm_env = np.maximum(0.0, np.exp(-((t % 2.0) * 4.0)))
    marimba = np.sin(2 * np.pi * 523.25 * t) * rhythm_env * 0.15 # C5
    marimba2 = np.sin(2 * np.pi * 392.00 * t) * np.roll(rhythm_env, int(sample_rate * 1.0)) * 0.10 # G4
    
    total_audio += marimba + marimba2
    
    # Normalização e atenuação para -22 dB sob a voz
    max_val = np.max(np.abs(total_audio))
    if max_val > 0:
        total_audio = total_audio / max_val
        
    # Nível de -22 dB = 10 ** (-22 / 20) = ~0.079
    total_audio = total_audio * 0.075
    
    # Fade in inicial (3s) e fade out final (4s)
    fade_in = np.clip(t / 3.0, 0.0, 1.0)
    fade_out = np.clip((duration - t) / 4.0, 0.0, 1.0)
    total_audio = total_audio * fade_in * fade_out
    
    # Converte para int16 estéreo
    audio_int16 = (total_audio * 32767).astype(np.int16)
    audio_stereo = np.column_stack((audio_int16, audio_int16))
    
    # Salva via scipy ou wave
    import wave
    with wave.open(output_path, "w") as wav_file:
        wav_file.setnchannels(2)
        wav_file.setsampwidth(2)
        wav_file.setframerate(sample_rate)
        wav_file.writeframes(audio_stereo.tobytes())
        
    print(f"Trilha sonora gerada com sucesso em {output_path}!")

if __name__ == "__main__":
    generate_calm_ambient_track()
