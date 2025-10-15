#!/usr/bin/env python3
# -*- coding: utf-8 -*-
import re
import argparse
import logging
from pathlib import Path
from typing import Iterator, Optional

# Regex para identificar linhas de cabeçalho/rodapé de página
PAGE_HEADER_RE = re.compile(r"^\s*---\s*Página\s*\d+\s*---\s*$", re.I)
PAGE_NUMBER_RE = re.compile(r"^\s*\d+\s*$")
TOC_LINE_RE    = re.compile(r"^\s*\d+(?:[\.\s]\d+)*\s+.*")

# Regex para capturar sequências de "palavras" totalmente em maiúsculas
UPPER_SEQ_RE = re.compile(
    r'\b[ÁÉÍÓÚÂÊÔÃÕÇA-Z]{2,}(?:\s+[ÁÉÍÓÚÂÊÔÃÕÇA-Z]{2,})*\b'
)

# Regex para detectar final de frase
END_PUNCT_RE = re.compile(r'[\.!\?…]$')

def is_mostly_upper(line: str, threshold: float = 0.8) -> bool:
    """
    Retorna True se a proporção de letras maiúsculas for >= threshold.
    """
    letters = [c for c in line if c.isalpha()]
    if not letters:
        return False
    upper = sum(1 for c in letters if c.isupper())
    return (upper / len(letters)) >= threshold

def strip_upper_sequences(line: str) -> str:
    """
    Remove trechos inteiros em maiúsculas dentro de uma linha.
    """
    return UPPER_SEQ_RE.sub('', line)

def should_skip_line(stripped: str) -> bool:
    """
    Verifica se a linha deve ser descartada:
    - cabeçalho/rodapé de página
    - número isolado
    - linha de sumário
    - linha com quase todas as letras em maiúsculas
    """
    if PAGE_HEADER_RE.match(stripped):
        logging.debug(f"Descartando cabeçalho: {stripped!r}")
        return True
    if PAGE_NUMBER_RE.match(stripped):
        logging.debug(f"Descartando número de página: {stripped!r}")
        return True
    if TOC_LINE_RE.match(stripped):
        logging.debug(f"Descartando sumário: {stripped!r}")
        return True
    if is_mostly_upper(stripped, threshold=1.0):
        logging.debug(f"Descartando linha totalmente maiúscula: {stripped!r}")
        return True
    return False

def clean_pdf_text(lines: Iterator[str]) -> Iterator[str]:
    buffer: Optional[str] = None
    prev_line: Optional[str] = None

    for raw in lines:
        line = raw.rstrip('\n')
        stripped = line.strip()

        # 1. descarta linhas indesejadas
        if should_skip_line(stripped):
            continue

        # 2. dessete hifenização
        if line.endswith('-'):
            buffer = (buffer or '') + line[:-1]
            continue
        if buffer is not None:
            line = buffer + line.lstrip()
            buffer = None

        # 3. remove seq. maiúsculas embutidas
        line = strip_upper_sequences(line).strip()
        if not line:
            continue

        # 4. junta parágrafos sem pontuação final
        if prev_line is not None and not END_PUNCT_RE.search(prev_line):
            prev_line += ' ' + line.lstrip()
            continue

        # 5. se chegou aqui, é nova linha/parágrafo
        if prev_line is not None:
            yield prev_line
        prev_line = line

    # não esquecer de emitir a última
    if prev_line is not None:
        yield prev_line

def main():
    parser = argparse.ArgumentParser(
        description="Limpa texto extraído de PDF: remove cabeçalhos, sumários, seq. maiúsculas, dessete hifenização e junta parágrafos."
    )
    parser.add_argument("input",  type=Path, help="Arquivo de entrada (texto extraído).")
    parser.add_argument("output", type=Path, help="Arquivo de saída (limpo).")
    parser.add_argument(
        "-v", "--verbose", action="store_true",
        help="Mostra logs de debug."
    )
    args = parser.parse_args()

    logging.basicConfig(
        level=logging.DEBUG if args.verbose else logging.INFO,
        format="%(levelname)s: %(message)s"
    )

    with args.input.open(encoding="utf-8") as f_in:
        cleaned = list(clean_pdf_text(f_in))

    with args.output.open("w", encoding="utf-8") as f_out:
        for ln in cleaned:
            # garante linha em branco entre parágrafos
            f_out.write(ln + "\n\n")

    logging.info(f"Texto limpo salvo em: {args.output}")

if __name__ == "__main__":
    main()

