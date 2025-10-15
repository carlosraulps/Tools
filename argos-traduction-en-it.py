
#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import subprocess
import argparse
from pathlib import Path
from tqdm import tqdm

import argostranslate.package as package
import argostranslate.translate as translate

def install_en_it():
    """
    Atualiza o índice de pacotes e instala o pacote English->Italian, se ainda não estiver instalado.
    """
    # 1. Atualiza o índice remoto de pacotes
    subprocess.run(["argospm", "update"], check=True)

    # 2. Verifica se já existe um pacote instalado en->it
    installed = package.get_installed_packages()
    if not any(p.from_code == "en" and p.to_code == "it" for p in installed):
        # 3. Se não houver, baixa e instala o modelo
        available = package.get_available_packages()
        pkg = next(p for p in available if p.from_code == "en" and p.to_code == "it")
        package.install_from_path(pkg.download())

    # 4. Lista os pacotes instalados (confirma a instalação)
    subprocess.run(["argospm", "list"], check=True)

def load_translation_model():
    """
    Carrega o objeto de tradução (ITranslation) para en->it usando as APIs do Argos Translate.
    """
    # Garante que o pacote esteja instalado
    install_en_it()

    # Obtém as línguas instaladas
    langs = translate.get_installed_languages()

    # Seleciona as línguas de origem e destino
    from_lang = next(l for l in langs if l.code == "en")
    to_lang   = next(l for l in langs if l.code == "it")

    # Obtém o objeto de tradução
    translation = from_lang.get_translation(to_lang)
    if translation is None:
        raise RuntimeError("Não foi possível carregar o modelo de tradução en->it.")
    return translation

def translate_file(input_path: Path, output_path: Path, translation):
    """
    Traduz cada linha do arquivo, mostrando uma barra de progresso.
    """
    lines = input_path.read_text(encoding="utf-8").splitlines()
    translated = []
    for line in tqdm(lines, desc="Traduzindo linhas", unit="linha"):
        translated.append(translation.translate(line))
    output_path.write_text("\n".join(translated), encoding="utf-8")
    print(f"✅ Tradução concluída e salva em: {output_path}")

def main():
    parser = argparse.ArgumentParser(
        description="Traduz um arquivo EN->IT usando Argos Translate com barra de progresso."
    )
    parser.add_argument("input",  help="Arquivo de entrada (texto em inglês).")
    parser.add_argument("output", help="Arquivo de saída (texto traduzido).")
    args = parser.parse_args()

    translation = load_translation_model()
    translate_file(Path(args.input), Path(args.output), translation)

if __name__ == "__main__":
    main()

