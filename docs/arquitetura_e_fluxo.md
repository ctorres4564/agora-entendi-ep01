# Arquitetura e Fluxo de Produção Automatizada — Agora Entendi

## 1. Visão Geral da Arquitetura

O sistema de produção de vídeo do canal **Agora Entendi** foi desenhado para ser determinístico, modular e auditável. Ele transforma um roteiro estruturado com marcações de conceitos em um vídeo final 1080p sincronizado por frame.

```
                  ┌───────────────────────────────┐
                  │   Roteiro em JSON / Python    │
                  │   (prompts/roteiro_prompts.md)│
                  └──────────────┬────────────────┘
                                 │
                 ┌───────────────┴───────────────┐
                 ▼                               ▼
      ┌──────────────────────┐        ┌──────────────────────┐
      │  TTS Neural Engine   │        │   Music Generator    │
      │  (edge-tts pt-BR)    │        │   (Harmonic Synth)   │
      └──────────┬───────────┘        └──────────┬───────────┘
                 │                               │
                 ├─────────────────┐             │
                 ▼                 ▼             │
      ┌──────────────────┐  ┌──────────────┐     │
      │ timeline_cenas   │  │ legendas.srt │     │
      │ (timestamps JSON)│  └──────────────┘     │
      └──────────┬───────┘                       │
                 │                               │
                 ▼                               │
      ┌──────────────────────────────────┐       │
      │    Scene Renderer (Pillow)       │       │
      │  - 2D Flat Motion Graphics       │       │
      │  - Mapa do Episódio Modular      │       │
      │  - Montserrat ExtraBold (≤5 w)   │       │
      └──────────────────┬───────────────┘       │
                         │                       │
                         ▼                       │
      ┌──────────────────────────────────────────┴─────┐
      │            FFmpeg Compositor Engine            │
      │  - Concat Demuxer por Frame                    │
      │  - Mixagem de Áudio (Voz + Trilha a -22 dB)    │
      │  - Encode H.264 / AAC 1080p 30fps              │
      └──────────────────┬─────────────────────────────┘
                         │
                         ▼
             [ output/agora_entendi_ep01_1080p.mp4 ]
```

---

## 2. Fluxo de Dados

1. **Entrada de Roteiro:**
   - O roteiro é fragmentado em blocos conceituais e parágrafos/frases em `scripts/generate_narration.py`.
2. **Síntese e Alinhamento:**
   - Cada segmento é gerado individualmente com a voz `pt-BR-AntonioNeural` a uma taxa de fala de `+6%` e pausas de 0,35s entre frases e 0,65s entre blocos.
   - A duração de cada segmento é computada via `mutagen` e gravada no arquivo de controle `assets/audio/timeline_cenas.json`.
   - As legendas `.srt` são compiladas automaticamente em `output/legendas.srt`.
3. **Geração Gráfica e Composição Visual:**
   - O serviço `services/scene_renderer.py` desenha cada uma das 107 cenas com base nas propriedades de cada segmento:
     - Estado dos nós no mini-mapa (`components/episode_map.py`);
     - Paleta (#F5F1EA nas explicativas, #14213D nas noturnas);
     - Tipografia oficial (`components/typography.py`);
     - Ilustrações 2D pedagógicas.
4. **Mixagem e Render Final:**
   - `scripts/render_video.py` utiliza o demuxer `ffconcat` para reproduzir cada imagem durante seu intervalo exato, combinando com o áudio master da narração e a trilha de fundo suavizada em -22 dB.

---

## 3. Como Manter e Expandir para Novos Episódios

Para produzir o **Episódio #2: Como o cérebro aprende?**:
1. Copie o arquivo `prompts/roteiro_e_prompts.md` e insira o novo roteiro com as marcações de nós e textos na tela.
2. Atualize o dicionário `SCRIPT_DATA` em `scripts/generate_narration.py`.
3. Execute sequencialmente:
   ```bash
   python scripts/generate_narration.py
   python scripts/generate_music.py
   python scripts/generate_scenes.py
   python scripts/generate_thumbnail.py
   python scripts/render_video.py
   ```
4. Os arquivos finais serão depositados automaticamente na pasta `/output`.
