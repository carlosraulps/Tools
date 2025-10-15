
import re

def reconstruir_oracoes(caminho_arquivo):
    with open(caminho_arquivo, 'r', encoding='utf-8') as f:
        linhas = f.readlines()

    texto_corrigido = []
    buffer = ""

    # Regex para detectar final de sentença
    fim_oracao = re.compile(r'[.!?…]["»”’\)]?\s*$')

    for linha in linhas:
        linha_strip = linha.strip()
        
        if not linha_strip:
            # Linha em branco indica quebra legítima de parágrafo
            if buffer:
                texto_corrigido.append(buffer.strip())
                buffer = ""
            texto_corrigido.append("")  # Preserva a quebra
        else:
            if buffer:
                # Verifica se a linha anterior terminou uma oração
                if fim_oracao.search(buffer):
                    texto_corrigido.append(buffer.strip())
                    buffer = linha_strip
                else:
                    buffer += " " + linha_strip
            else:
                buffer = linha_strip

    # Adiciona a última linha se ainda houver algo
    if buffer:
        texto_corrigido.append(buffer.strip())

    # Salva em novo arquivo
    caminho_saida = caminho_arquivo.replace(".txt", "_unido.txt")
    with open(caminho_saida, 'w', encoding='utf-8') as f:
        for linha in texto_corrigido:
            f.write(linha + '\n')

    print(f"Arquivo salvo como: {caminho_saida}")

# Use o caminho do seu arquivo aqui:
reconstruir_oracoes('translated_it.txt')
