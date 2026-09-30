# Agora Entendi — Ep. 01: Neurociência do Zero

Repositório de produção automatizada do canal de YouTube **Agora entendi — Assuntos difíceis. Explicados do começo.**

## Objetivo do Projeto
Produção completa do primeiro episódio do canal, abordando os conceitos fundamentais da neurociência (Neurônio, Sinapse, Neurotransmissores, Redes Cerebrais, Plasticidade, Memória, Atenção e Sono) em formato faceless, motion graphics 2D flat, com narração neural de alta naturalidade em pt-BR e mapa conceitual evolutivo.

## Stack Utilizada
- **Linguagem & Runtime:** Python 3.12 / Node.js
- **Síntese de Voz (TTS):** Microsoft Edge TTS Neural (`pt-BR-AntonioNeural` / `pt-BR-FranciscaNeural`)
- **Manipulação & Composição Gráfica:** Pillow (PIL), NumPy, Canvas/SVG renderer
- **Renderização e Mixagem Audiovisual:** FFmpeg
- **Gerenciador de Versão:** Git

## Instruções de Instalação e Execução
1. **Pré-requisitos:**
   - Python 3.12+ instalado com pip
   - FFmpeg instalado e acessível no PATH do sistema

2. **Instalação das Dependências:**
   ```bash
   pip install edge-tts pillow numpy
   ```

3. **Geração do Episódio:**
   - Geração de Narração e Legendas:
     ```bash
     python scripts/generate_narration.py
     ```
   - Geração dos Assets Visuais e Mapa:
     ```bash
     python scripts/generate_scenes.py
     ```
   - Composição Final e Render do Vídeo:
     ```bash
     python scripts/render_video.py
     ```

## Estrutura de Diretórios
```
/
├── .gitignore
├── README.md
├── /assets            # Elementos estáticos, áudio, trilhas e texturas
│   ├── /audio
│   ├── /images
│   └── /thumbnails
├── /components        # Módulos gráficos reutilizáveis (nós, tipografia)
├── /docs              # Documentação e relatórios técnicos de produção
├── /pages             # Definições estruturais de quadros/telas
├── /prompts           # Registro de roteiro e parâmetros de geração
├── /scripts           # Scripts automatizados de processamento e render
├── /services          # Motores de TTS, animação e áudio
├── /src               # Código-fonte auxiliar
└── /utils             # Formatadores, helpers de tempo e matemática
```
