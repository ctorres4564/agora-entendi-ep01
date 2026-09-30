import asyncio
import os
import json
import edge_tts
import subprocess

SCRIPT_DATA = [
    {
        "id": "abertura",
        "title": "ABERTURA",
        "on_screen_text": "DOPAMINA = PRAZER?",
        "node": None,
        "paragraphs": [
            "Você provavelmente já ouviu falar em dopamina.",
            "Talvez tenha ouvido que ela é a substância do prazer.",
            "Que, quando você come um chocolate ou recebe uma curtida, o cérebro solta dopamina e você se sente bem.",
            "Não é exatamente assim.",
            "E para entender por quê, precisamos começar por uma coisa muito menor.",
            "Uma única célula: um neurônio."
        ]
    },
    {
        "id": "conceito_1",
        "title": "CONCEITO 1 — NEURÔNIO",
        "on_screen_text": "86 BILHÕES DE NEURÔNIOS",
        "node": "neurônio",
        "paragraphs": [
            "Seu cérebro é feito de células, como o resto do corpo.",
            "Mas algumas delas têm uma especialidade: receber e enviar sinais. Essas células são os neurônios.",
            "Um neurônio tem ramificações curtas, que recebem mensagens, e um prolongamento mais longo, que leva a mensagem adiante.",
            "Por dentro dele, a mensagem viaja como um pequeno impulso elétrico.",
            "Você usa isso o tempo todo.",
            "Quando encosta a mão numa panela quente e puxa antes mesmo de pensar \"está quente\", foram neurônios passando sinais em sequência, muito rápido.",
            "E quantos neurônios existem no cérebro?",
            "Durante décadas, os livros repetiram: cem bilhões.",
            "Até que uma neurocientista brasileira, Suzana Herculano-Houzel, resolveu contar de verdade, num laboratório no Rio de Janeiro.",
            "O resultado: cerca de 86 bilhões. Menos do que se dizia. Mas ainda uma quantidade enorme.",
            "Só que um neurônio sozinho não faz nada. O interessante é como ele passa o recado para o próximo."
        ]
    },
    {
        "id": "conceito_2",
        "title": "CONCEITO 2 — SINAPSE",
        "on_screen_text": "SINAPSE",
        "node": "sinapse",
        "paragraphs": [
            "Imagine uma fila de pessoas passando um recado de ouvido em ouvido.",
            "O recado precisa pular de uma pessoa para a próxima.",
            "No cérebro, o ponto onde um neurônio passa o recado para outro tem nome: sinapse.",
            "E aqui está uma surpresa.",
            "Muita gente imagina o cérebro como fios elétricos emendados uns nos outros.",
            "Mas, na maioria das sinapses, os neurônios nem se encostam.",
            "Existe um espaço minúsculo entre eles, milhares de vezes mais fino que um fio de cabelo.",
            "O sinal elétrico chega ao fim de um neurônio e para ali. Não consegue saltar sozinho.",
            "Então, como o recado atravessa?"
        ]
    },
    {
        "id": "conceito_3",
        "title": "CONCEITO 3 — NEUROTRANSMISSOR",
        "on_screen_text": "QUERER ≠ GOSTAR",
        "node": "neurotransmissor",
        "paragraphs": [
            "Ele atravessa na forma de química.",
            "Quando o sinal chega ao fim do neurônio, ele libera pequenas substâncias nesse espaço.",
            "Elas cruzam e se encaixam no neurônio seguinte, como uma chave numa fechadura.",
            "Essas substâncias se chamam neurotransmissores.",
            "Existem dezenas deles. E um é famoso: a dopamina.",
            "Agora dá para voltar à pergunta do começo. A dopamina é a substância do prazer?",
            "Nos anos 1980, o pesquisador Kent Berridge tentou provar exatamente isso em ratos. E o resultado surpreendeu até ele.",
            "Ratos que ficavam praticamente sem dopamina deixavam de buscar comida.",
            "Mas, quando o alimento era colocado na boca deles, ainda mostravam sinais de que gostavam.",
            "Ou seja: a dopamina tem mais a ver com querer do que com gostar.",
            "Com a motivação de ir atrás de algo, e com aprender o que vale a pena buscar.",
            "Ela também participa de outras funções, como o controle dos movimentos.",
            "Isso ajuda a entender por que você pode sentir vontade de abrir o celular a cada vibração, mesmo quando o que encontra lá nem é tão bom assim."
        ]
    },
    {
        "id": "conceito_4",
        "title": "CONCEITO 4 — REDES CEREBRAIS",
        "on_screen_text": "MITO DOS 10%",
        "node": "redes",
        "paragraphs": [
            "Com 86 bilhões de neurônios trocando recados, o cérebro não funciona como uma sala com um único chefe.",
            "Funciona mais como uma cidade.",
            "Regiões diferentes têm especialidades.",
            "Umas lidam mais com a visão, outras com os movimentos, outras com a linguagem.",
            "Mas quase nada acontece numa região só.",
            "Quando você atende o telefone e reconhece a voz da sua mãe na primeira palavra, áreas ligadas à audição, à memória e à emoção estão trabalhando juntas.",
            "Esses conjuntos de regiões conectadas são chamados de redes.",
            "É aqui que cai um mito famoso: o de que usamos só 10% do cérebro.",
            "Exames de imagem mostram atividade no cérebro inteiro ao longo do dia.",
            "Não tudo ao mesmo tempo, com a mesma intensidade.",
            "Numa cidade, nem todas as luzes ficam acesas a toda hora. Mas nenhum bairro está abandonado.",
            "E essa cidade não fica igual para sempre."
        ]
    },
    {
        "id": "conceito_5",
        "title": "CONCEITO 5 — PLASTICIDADE",
        "on_screen_text": "O CÉREBRO MUDA COM O USO",
        "node": "plasticidade",
        "paragraphs": [
            "Pense numa trilha num gramado.",
            "Quando muita gente passa pelo mesmo caminho, ele fica marcado. Quando ninguém passa, o mato volta a crescer.",
            "As conexões entre neurônios se comportam de um jeito parecido.",
            "As que são muito usadas se fortalecem. As que ficam sem uso enfraquecem.",
            "Essa capacidade do cérebro de mudar com a experiência tem nome: plasticidade.",
            "Lembra das primeiras aulas de direção?",
            "Trocar a marcha, olhar o retrovisor e controlar a embreagem exigiam toda a sua atenção.",
            "Meses depois, você faz tudo isso conversando.",
            "Essa mudança não aconteceu só no seu comportamento. Aconteceu nas conexões do seu cérebro.",
            "A analogia da trilha tem um limite: o cérebro não só aprofunda caminhos antigos.",
            "Ele também cria ligações novas e reorganiza as que já existem.",
            "E um erro comum é achar que isso só acontece na infância.",
            "A plasticidade é maior quando somos crianças, mas continua pela vida toda.",
            "Um adulto que aprende a tocar um instrumento também está mudando o próprio cérebro."
        ]
    },
    {
        "id": "conceito_6",
        "title": "CONCEITO 6 — MEMÓRIA",
        "on_screen_text": "LEMBRAR É RECONSTRUIR",
        "node": "memória",
        "paragraphs": [
            "Se as conexões mudam quando você vive alguma coisa, é aí que mora a memória.",
            "E isso muda o jeito de pensar sobre lembranças.",
            "A gente costuma imaginar a memória como um arquivo de computador: você guarda, depois abre, e ele está igualzinho. Não é assim.",
            "Uma lembrança fica espalhada em pedaços, em várias partes da rede.",
            "Quando você lembra, o cérebro junta esses pedaços de novo. Ele reconstrói.",
            "E, nesse processo, pode preencher lacunas, misturar detalhes de outras situações e até incluir coisas que não aconteceram.",
            "É por isso que dois irmãos podem contar a mesma festa de família de jeitos diferentes, os dois com toda a certeza.",
            "Nenhum deles está necessariamente mentindo. Cada um reconstruiu a lembrança à sua maneira.",
            "A psicóloga Elizabeth Loftus mostrou, em vários experimentos, que até a forma de fazer uma pergunta pode mudar o que a pessoa lembra.",
            "Mas, para algo virar memória, primeiro precisa entrar."
        ]
    },
    {
        "id": "conceito_7",
        "title": "CONCEITO 7 — ATENÇÃO",
        "on_screen_text": "MULTITAREFA = ALTERNAR",
        "node": "atenção",
        "paragraphs": [
            "A todo instante, chegam ao seu cérebro sons, imagens, cheiros, sensações do corpo.",
            "Se tudo tivesse o mesmo peso, seria impossível pensar.",
            "Por isso existe um filtro que decide o que ganha prioridade. Esse filtro é a atenção.",
            "Funciona como um holofote num palco escuro.",
            "O que está sob a luz fica nítido. O resto continua lá, mas em segundo plano.",
            "Você já deve ter vivido isso numa festa barulhenta.",
            "Você não presta atenção nas conversas ao redor, até que alguém do outro lado fala o seu nome.",
            "Muitas vezes, na hora, o holofote vira para lá.",
            "E aqui está o erro comum: a multitarefa.",
            "Quando duas tarefas exigem atenção, como escrever uma mensagem e acompanhar uma aula, o cérebro não faz as duas ao mesmo tempo.",
            "Ele alterna entre elas. E cada troca custa tempo e aumenta a chance de erro.",
            "Agora, o que acontece com tudo isso quando você apaga a luz e vai dormir?"
        ]
    },
    {
        "id": "conceito_8",
        "title": "CONCEITO 8 — SONO",
        "on_screen_text": "O CÉREBRO NÃO DESLIGA",
        "node": "sono",
        "paragraphs": [
            "Muita gente imagina que, durante o sono, o cérebro desliga para descansar. Não é o que acontece.",
            "Pesquisadores que acompanharam a atividade do cérebro durante a noite viram algo curioso:",
            "regiões usadas para aprender algo durante o dia voltam a ficar ativas no sono seguinte.",
            "Em ratos, dá para ver até os mesmos neurônios disparando na mesma ordem, só que mais rápido.",
            "É como se o cérebro repassasse o que foi vivido.",
            "Esse repasse ajuda a fortalecer as lembranças novas e a encaixá-las no que você já sabia. O nome disso é consolidação.",
            "É por isso que uma noite de sono depois de estudar faz diferença.",
            "E também por que aquele problema que parecia sem saída às vezes fica mais claro de manhã.",
            "Uma ressalva: o sono ajuda a guardar o que você aprendeu acordado.",
            "Ouvir uma aula dormindo não é um jeito de aprender o conteúdo."
        ]
    },
    {
        "id": "fechamento",
        "title": "FECHAMENTO",
        "on_screen_text": "COMO O CÉREBRO APRENDE?",
        "node": "fechamento_mapa",
        "paragraphs": [
            "Então vamos juntar as peças.",
            "Neurônios são células que enviam sinais.",
            "Eles se comunicam nas sinapses, por meio de neurotransmissores, como a dopamina, que tem mais a ver com querer do que com gostar.",
            "Esses neurônios formam redes espalhadas pelo cérebro inteiro.",
            "E essas redes mudam com o uso: isso é plasticidade.",
            "É nessa mudança que mora a memória, que depende do que a atenção deixou entrar e que o sono ajuda a fixar.",
            "Esse é o mapa básico do seu cérebro.",
            "Mas ele deixa uma pergunta no ar.",
            "Se o cérebro muda toda vez que você aprende, o que exatamente acontece quando você aprende alguma coisa?",
            "É o que a gente vê no próximo vídeo."
        ]
    }
]

def format_srt_time(seconds: float) -> str:
    hrs = int(seconds // 3600)
    mins = int((seconds % 3600) // 60)
    secs = int(seconds % 60)
    millis = int(round((seconds - int(seconds)) * 1000))
    if millis >= 1000:
        secs += 1
        millis = 0
    return f"{hrs:02d}:{mins:02d}:{secs:02d},{millis:03d}"

def get_audio_duration(file_path: str) -> float:
    from mutagen.mp3 import MP3
    from mutagen.wave import WAVE
    if file_path.lower().endswith('.mp3'):
        audio = MP3(file_path)
        return float(audio.info.length)
    elif file_path.lower().endswith('.wav'):
        audio = WAVE(file_path)
        return float(audio.info.length)
    else:
        import mutagen
        audio = mutagen.File(file_path)
        return float(audio.info.length)

async def generate_speech_segment(text: str, output_path: str, voice: str = "pt-BR-AntonioNeural", rate: str = "+6%"):
    communicate = edge_tts.Communicate(text, voice, rate=rate)
    await communicate.save(output_path)

async def main():
    os.makedirs("assets/audio/segments", exist_ok=True)
    os.makedirs("output", exist_ok=True)
    
    srt_entries = []
    timeline = []
    srt_index = 1
    current_time = 0.0
    
    file_list_path = "assets/audio/concat_list.txt"
    with open(file_list_path, "w", encoding="utf-8") as concat_f:
        pass
        
    concat_lines = []

    print("Iniciando geração de narração com voz natural pt-BR-AntonioNeural (calibrada para ~9:45)...")
    
    for block_idx, block in enumerate(SCRIPT_DATA):
        print(f"\nProcessando Bloco {block_idx}: {block['title']}...")
        block_start = current_time
        
        for p_idx, paragraph in enumerate(block["paragraphs"]):
            seg_filename = f"assets/audio/segments/seg_{block_idx:02d}_{p_idx:02d}.mp3"
            
            # Gera TTS para a frase com taxa ajustada
            await generate_speech_segment(paragraph, seg_filename, voice="pt-BR-AntonioNeural", rate="+6%")
            dur = get_audio_duration(seg_filename)
            
            p_start = current_time
            p_end = current_time + dur
            
            # Registra no SRT
            srt_entries.append(
                f"{srt_index}\n{format_srt_time(p_start)} --> {format_srt_time(p_end)}\n{paragraph}\n"
            )
            srt_index += 1
            
            timeline.append({
                "block_id": block["id"],
                "block_title": block["title"],
                "paragraph_idx": p_idx,
                "text": paragraph,
                "start": p_start,
                "end": p_end,
                "duration": dur,
                "file": seg_filename,
                "on_screen_text": block["on_screen_text"],
                "node": block["node"]
            })
            
            concat_lines.append(f"file '{os.path.abspath(seg_filename)}'")
            current_time = p_end
            
            # Pausa entre frases/parágrafos (~0.35s)
            pause_time = 0.35
            silence_file = f"assets/audio/segments/silence_{pause_time:.2f}s.mp3"
            if not os.path.exists(silence_file):
                subprocess.run([
                    "ffmpeg", "-y", "-f", "lavfi", "-i", f"anullsrc=r=24000:cl=mono",
                    "-t", str(pause_time), "-q:a", "9", silence_file
                ], stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)
            concat_lines.append(f"file '{os.path.abspath(silence_file)}'")
            current_time += pause_time
            
        # Pausa adicional entre blocos (~0.65s para somar ~1.0s total entre blocos)
        block_pause = 0.65
        block_silence_file = f"assets/audio/segments/silence_block_{block_pause:.2f}s.mp3"
        if not os.path.exists(block_silence_file):
            subprocess.run([
                "ffmpeg", "-y", "-f", "lavfi", "-i", f"anullsrc=r=24000:cl=mono",
                "-t", str(block_pause), "-q:a", "9", block_silence_file
            ], stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)
        concat_lines.append(f"file '{os.path.abspath(block_silence_file)}'")
        current_time += block_pause
        
        print(f"Bloco {block['title']} concluído: {block_start:.2f}s até {current_time:.2f}s")

    # Salva concat_list
    with open(file_list_path, "w", encoding="utf-8") as concat_f:
        for line in concat_lines:
            concat_f.write(line.replace("\\", "/") + "\n")
            
    # Concatena em MP3 e WAV de alta qualidade
    output_mp3 = "output/narracao_isolada.mp3"
    output_wav = "output/narracao_isolada.wav"
    print(f"\nConcatenando narração master em {output_mp3} e {output_wav}...")
    
    subprocess.run([
        "ffmpeg", "-y", "-f", "concat", "-safe", "0", "-i", file_list_path,
        "-c:a", "libmp3lame", "-q:a", "0", output_mp3
    ], check=True)
    
    subprocess.run([
        "ffmpeg", "-y", "-i", output_mp3,
        "-ar", "48000", "-ac", "2", output_wav
    ], check=True)
    
    final_dur = get_audio_duration(output_mp3)
    minutes = int(final_dur // 60)
    seconds = int(final_dur % 60)
    print(f"\n>>> DURAÇÃO FINAL DA NARRAÇÃO: {final_dur:.2f} s ({minutes:02d}:{seconds:02d}) <<<")
    
    # Salva SRT
    srt_path = "output/legendas.srt"
    with open(srt_path, "w", encoding="utf-8") as f:
        f.write("\n".join(srt_entries))
    print(f"Legendas salvas em {srt_path}")
    
    # Salva timeline
    timeline_path = "assets/audio/timeline_cenas.json"
    with open(timeline_path, "w", encoding="utf-8") as f:
        json.dump({
            "total_duration": final_dur,
            "blocks": SCRIPT_DATA,
            "timeline": timeline
        }, f, indent=2, ensure_ascii=False)
    print(f"Timeline salva em {timeline_path}")

if __name__ == "__main__":
    asyncio.run(main())
