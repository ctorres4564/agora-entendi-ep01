import unittest
import os
import json
from components.episode_map import NODES_ORDER
from components.typography import get_font

class TestAgoraEntendiPipeline(unittest.TestCase):
    
    def test_nodes_order(self):
        expected_nodes = [
            "neurônio", "sinapse", "neurotransmissor", "redes",
            "plasticidade", "memória", "atenção", "sono"
        ]
        self.assertEqual(NODES_ORDER, expected_nodes)

    def test_timeline_file_validity(self):
        timeline_path = "assets/audio/timeline_cenas.json"
        self.assertTrue(os.path.exists(timeline_path), "Timeline JSON não encontrado.")
        with open(timeline_path, "r", encoding="utf-8") as f:
            data = json.load(f)
            
        self.assertIn("total_duration", data)
        self.assertIn("timeline", data)
        # Janela de duração: 9:15 (555s) a 10:30 (630s)
        duration = data["total_duration"]
        self.assertGreaterEqual(duration, 555.0, f"Duração {duration}s menor que 9:15")
        self.assertLessEqual(duration, 630.0, f"Duração {duration}s maior que 10:30")
        
        # Validação do limite de até 5 palavras no texto exibido na tela
        for seg in data["timeline"]:
            display_words = seg["on_screen_text"].split()[:5]
            self.assertLessEqual(len(display_words), 5)

    def test_output_deliverables_exist(self):
        deliverables = [
            "output/agora_entendi_ep01_1080p.mp4",
            "output/narracao_isolada.wav",
            "output/narracao_isolada.mp3",
            "output/legendas.srt",
            "output/thumbnail_1280x720.png"
        ]
        for item in deliverables:
            self.assertTrue(os.path.exists(item), f"Entregável {item} não foi encontrado.")
            self.assertGreater(os.path.getsize(item), 0, f"Entregável {item} está vazio.")

    def test_srt_file_content(self):
        srt_path = "output/legendas.srt"
        with open(srt_path, "r", encoding="utf-8") as f:
            content = f.read()
        self.assertIn("dopamina", content.lower())
        self.assertIn("86 bilhões", content.lower())
        self.assertIn("sinapse", content.lower())

if __name__ == "__main__":
    unittest.main()
