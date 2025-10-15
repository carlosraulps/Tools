#!/usr/bin/env python3
import re

def clean_pdf_text(input_txt: str, output_txt: str) -> None:
    """
    Limpa e formata melhor o texto extraído de um PDF:
    - Remove linhas tipo '--- Página X ---'
    - Une palavras hifenizadas no fim da linha
    - Junta linhas sem pontuação final ou em branco em parágrafos contínuos
    """
    with open(input_txt, encoding='utf-8') as f:
        lines = f.readlines()

    cleaned_lines = []
    buffer = ""

    for raw in lines:
        line = raw.rstrip("\n")

        # 1. Pula cabeçalhos de página
        if re.match(r"^---\s*Página\s*\d+\s*---$", line):
            continue

        # 2. Desfaz hifenização (palavra- \n sílaba → palavra+sílaba)
        if line.endswith('-'):
            buffer += line[:-1]
            continue  # continua acumulando no buffer

        # Acumula o restante
        if buffer:
            line = buffer + line
            buffer = ""

        # 3. Junta linhas sem pontuação final com a próxima
        if cleaned_lines:
            prev = cleaned_lines[-1]
            if prev and not re.search(r"[\.!\?\"']\s*$", prev):
                # se a linha anterior não terminou em ponto/?!/"'
                cleaned_lines[-1] = prev + " " + line.strip()
                continue

        cleaned_lines.append(line)

    # Escreve saída: uma linha em branco entre parágrafos
    with open(output_txt, 'w', encoding='utf-8') as f:
        for line in cleaned_lines:
            f.write(line + "\n")
            if not line.strip():
                f.write("\n")


if __name__ == "__main__":
    import sys
    if len(sys.argv) != 3:
        print("Uso: python3 clean_pdf_text.py in.txt out_clean.txt")
    else:
        clean_pdf_text(sys.argv[1], sys.argv[2])
        print(f"Texto limpo gravado em: {sys.argv[2]}")

