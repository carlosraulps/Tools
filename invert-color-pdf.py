
#!/usr/bin/env python3
import fitz  # pymupdf
from PIL import Image, ImageOps  # pip install pillow
import io

def invert_pdf(input_path: str,
               output_path: str,
               zoom: float = 1.0,
               jpeg_quality: int = 75) -> None:
    """
    Inverte cores de um PDF (fundo preto, texto branco), mantendo o arquivo
    com tamanho reduzido ao rasterizar em JPEG comprimido.

    :param input_path: caminho do PDF original
    :param output_path: caminho para o PDF invertido
    :param zoom: escala de renderização (1.0 = DPI original)
    :param jpeg_quality: qualidade JPEG de 1 a 100 (quanto menor, mais compressão)
    """
    doc = fitz.open(input_path)
    for page in doc:
        rect = page.rect

        # Renderiza em bitmap
        mat = fitz.Matrix(zoom, zoom)
        pix = page.get_pixmap(matrix=mat, alpha=False)

        # Converte Pixmap para PIL.Image
        mode = "RGB"  # sem canal alpha
        img = Image.frombytes(mode, (pix.width, pix.height), pix.samples)

        # Inverte cores via Pillow
        img = ImageOps.invert(img)

        # Limpa conteúdo vetorial original
        page.clean_contents()

        # Gera JPEG comprimido em memória
        buffer = io.BytesIO()
        img.save(buffer, format="JPEG", quality=jpeg_quality)
        img_bytes = buffer.getvalue()

        # Insere imagem JPEG esticada para ocupar toda a página
        page.insert_image(rect, stream=img_bytes, keep_proportion=False)

    # Salva com compressão adicional e limpeza de objetos não referenciados
    doc.save(output_path,
             deflate=True,
             clean=True,
             garbage=2)

    print(f"PDF invertido salvo em: {output_path}")

if __name__ == "__main__":
    import sys
    if len(sys.argv) != 3:
        print("Uso: invert-color-pdf.py input.pdf output_inverted.pdf")
    else:
        invert_pdf(sys.argv[1], sys.argv[2])

