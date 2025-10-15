
#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import re
from pathlib import Path

def clean_text(text: str) -> str:
    """
    Aplica várias etapas de limpeza:
    1. Remove linhas contendo 'oh mio dio' (case‐insensitive).
    2. Colapsa repetições adjacentes de palavras (e.g. 'ciao ciao' -> 'ciao').
    3. Remove espaços em excesso antes de pontuação.
    4. Garante um espaço após pontuação quando faltar.
    5. Remove espaços finais de cada linha.
    6. Colapsa múltiplas linhas em branco em no máximo duas.
    """
    # 1. Remove linhas com 'oh mio dio'
    text = re.sub(r'(?mi)^.*oh mio dio.*\n', '', text)  # :contentReference[oaicite:0]{index=0}

    # 2. Colapsa repetições de palavras
    text = re.sub(r'\b(\w+)(?:\s+\1\b)+', r'\1', text)  # :contentReference[oaicite:1]{index=1}

    # 3. Remove espaços antes de , . ; : ? !
    text = re.sub(r'\s+([,.;:?!])', r'\1', text)       # :contentReference[oaicite:2]{index=2}

    # 4. Garante um espaço após pontuação
    text = re.sub(r'([,.;:?!])([^\s])', r'\1 \2', text) 

    # 5. Remove espaços finais de cada linha
    text = re.sub(r'[ \t]+$', '', text, flags=re.MULTILINE)

    # 6. Colapsa mais de duas linhas em branco
    text = re.sub(r'\n{3,}', '\n\n', text)

    return text

def main():
    # Caminhos de entrada e saída
    input_file  = Path('translated_it.txt')             # :contentReference[oaicite:3]{index=3}
    output_file = Path('cleaned_translated_it.txt')

    # Lê, limpa e grava
    original = input_file.read_text(encoding='utf-8')
    cleaned  = clean_text(original)
    output_file.write_text(cleaned, encoding='utf-8')

    # Mostra as primeiras 20 linhas no terminal
    print("\nPrimeiras 20 linhas após limpeza:\n" + "-"*30)
    for idx, line in enumerate(cleaned.splitlines()[:20], start=1):
        print(f"{idx:2d}: {line}")

if __name__ == "__main__":
    main()

