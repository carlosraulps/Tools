
#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import re
import argparse

def replace_citations(text):
    """
    Substitui:
      :contentReference[oaicite:X]{index=Y}
    por
      [Y]
    e também casos entre parênteses:
      (:contentReference[...]...)
    por
      ([Y])
    """
    # 1) Tratamento de ocorrências com ou sem parênteses
    #    Ex.: "):contentReference[oaicite:36]{index=36}"
    #          ":contentReference[oaicite:12]{index=12}"
    pattern = re.compile(r"""
        \(?              # opcional abre parêntese
        :contentReference  # literal
        \[oaicite:\d+\]     # cit. oaicite:num
        \{index=(\d+)\}     # obtém o índice
        \)?              # opcional fecha parêntese
    """, re.VERBOSE)
    
    def _repl(m):
        idx = m.group(1)
        # Se veio com parênteses originais, mantém-os
        if m.group(0).startswith('(') and m.group(0).endswith(')'):
            return f'([{idx}])'
        else:
            return f'[{idx}]'
    
    return pattern.sub(_repl, text)

def process_file(input_path, output_path=None):
    with open(input_path, 'r', encoding='utf-8') as f:
        content = f.read()

    new_content = replace_citations(content)

    if not output_path:
        output_path = input_path

    with open(output_path, 'w', encoding='utf-8') as f:
        f.write(new_content)

if __name__ == "__main__":
    parser = argparse.ArgumentParser(
        description="Limpa :contentReference[oaicite:X]{index=Y} para [Y] no arquivo."
    )
    parser.add_argument('input_file', help="Arquivo de entrada (ex: input-ref.txt)")
    parser.add_argument('-o', '--output', help="Arquivo de saída (padrão: sobrescreve o de entrada)")
    args = parser.parse_args()

    process_file(args.input_file, args.output)
    print(f"Arquivo '{args.input_file}' processado.", end=' ')
    if args.output:
        print(f"Saída em '{args.output}'.")
    else:
        print("Arquivo original sobrescrito.")

