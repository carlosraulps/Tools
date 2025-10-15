
from transformers import MarianMTModel, MarianTokenizer
from pathlib import Path
from tqdm import tqdm  # Progress bar library

def batch_translate(
    input_path: str,
    output_path: str,
    model_name: str = "Helsinki-NLP/opus-mt-en-it",
    batch_size: int = 16
):
    # Load tokenizer and model
    tokenizer = MarianTokenizer.from_pretrained(model_name)  # :contentReference[oaicite:3]{index=3}
    model = MarianMTModel.from_pretrained(model_name)        # :contentReference[oaicite:4]{index=4}

    # Read all lines
    lines = Path(input_path).read_text(encoding="utf-8").splitlines()
    total_batches = (len(lines) + batch_size - 1) // batch_size

    translated_lines = []
    # Wrap the range iterator with tqdm to show progress
    for batch_start in tqdm(
        range(0, len(lines), batch_size),
        total=total_batches,
        desc="Translating batches",
        unit="batch"
    ):
        batch = lines[batch_start: batch_start + batch_size]
        # Tokenize and translate
        encoded = tokenizer(batch, return_tensors="pt", padding=True, truncation=True)
        outputs = model.generate(**encoded)
        decoded = [tokenizer.decode(t, skip_special_tokens=True) for t in outputs]
        translated_lines.extend(decoded)

    # Write translations to output file
    Path(output_path).write_text("\n".join(translated_lines), encoding="utf-8")
    print(f"✅ Translation complete: {output_path}")

# Usage example
if __name__ == "__main__":
    batch_translate(
        "Mortimer-Come-leggere-un-libro.txt",
        "translated_it.txt",
        model_name="Helsinki-NLP/opus-mt-en-it",
        batch_size=16
    )

