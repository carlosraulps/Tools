# GEMINI File Analysis

This document provides a detailed analysis of the files present in the `/Users/apple/Research/tools` directory. The scripts primarily focus on text processing, translation, PDF manipulation, and multimedia (music) downloading and tagging.

## Table of Contents

- [Text Processing & Translation](#text-processing--translation)
  - [argos-traduction-en-it.py](#argos-traduction-en-itpy)
  - [cleaning-mariam-traduction.py](#cleaning-mariam-traductionpy)
  - [en-it-traslation-osllm.py](#en-it-traslation-osllmpy)
  - [final-cleaner.py](#final-cleanerpy)
  - [cleaner-ref.py](#cleaner-refpy)
  - [postprocess-txt.py](#postprocess-txtpy)
  - [text-reconstruction.py](#text-reconstructionpy)
- [PDF Manipulation](#pdf-manipulation)
  - [invert-color-pdf.py](#invert-color-pdfpy)
- [Multimedia (Audio/Music)](#multimedia-audiomusic)
  - [auto_tagger.py](#auto_taggerpy)
  - [playlist-dowloader.py](#playlist-dowloaderpy)
  - [spotify-dowloader.py](#spotify-dowloaderpy)
- [Data](#data)
  - [v1-lamica-geniale.txt](#v1-lamica-genialetxt)

---

## Text Processing & Translation

### `argos-traduction-en-it.py`
*   **Description:** Translates a text file from English to Italian using the Argos Translate library (offline NMT).
*   **Key Features:**
    *   Automatically installs the English->Italian translation package if missing.
    *   Reads input line by line and translates using `argostranslate`.
    *   Uses `tqdm` to display a progress bar.
*   **Usage:** `python argos-traduction-en-it.py <input_file> <output_file>`

### `cleaning-mariam-traduction.py`
*   **Description:** Performs post-processing cleanup on Italian text, likely output from a translation tool.
*   **Key Features:**
    *   Removes specific artifacts (e.g., lines with "oh mio dio").
    *   Collapses repeated adjacent words.
    *   Fixes spacing around punctuation.
    *   Normalizes line breaks (removing excess blank lines).
    *   Hardcoded input/output filenames: `translated_it.txt` -> `cleaned_translated_it.txt`.
*   **Usage:** `python cleaning-mariam-traduction.py` (Edit script for file paths).

### `en-it-traslation-osllm.py`
*   **Description:** Translates text from English to Italian using the Hugging Face `transformers` library with the MarianMT model (`Helsinki-NLP/opus-mt-en-it`).
*   **Key Features:**
    *   Uses batch processing for efficiency.
    *   Includes a progress bar via `tqdm`.
    *   Hardcoded input/output in the `__main__` block (`Mortimer-Come-leggere-un-libro.txt` -> `translated_it.txt`).
*   **Usage:** `python en-it-traslation-osllm.py` (Edit script for file paths).

### `final-cleaner.py`
*   **Description:** Advanced text cleaner specifically designed for text extracted from PDFs.
*   **Key Features:**
    *   Removes page headers/footers (regex matching "Página X").
    *   Removes standalone numbers (page numbers) and TOC lines.
    *   Removes sequences of uppercase words (likely headers).
    *   De-hyphenates words split across lines.
    *   Merges paragraphs split across pages or lines.
    *   Uses `logging` for debug information.
*   **Usage:** `python final-cleaner.py <input_file> <output_file> [-v]`

### `cleaner-ref.py`
*   **Description:** Specifically targets and reformats citation references in the text.
*   **Key Features:**
    *   Replaces patterns like `:contentReference[oaicite:X]{index=Y}` with `[Y]`.
    *   Handles cases with or without surrounding parentheses.
*   **Usage:** `python cleaner-ref.py <input_file> [-o output_file]`

### `postprocess-txt.py`
*   **Description:** Basic cleaner for PDF extracted text.
*   **Key Features:**
    *   Removes page headers ("--- Página X ---").
    *   Fixes hyphenation at line ends.
    *   Joins lines that do not end in punctuation to reconstruct paragraphs.
*   **Usage:** `python postprocess-txt.py <input_file> <output_file>`

### `text-reconstruction.py`
*   **Description:** Reconstructs sentences/paragraphs from line-broken text.
*   **Key Features:**
    *   Merges lines into paragraphs until a sentence-ending punctuation mark is found.
    *   Preserves legitimate paragraph breaks (blank lines).
    *   Hardcoded input `translated_it.txt`.
*   **Usage:** `python text-reconstruction.py` (Edit script for file paths).

## PDF Manipulation

### `invert-color-pdf.py`
*   **Description:** Inverts the colors of a PDF (creating a "dark mode" effect) by rasterizing pages to images.
*   **Key Features:**
    *   Uses `pymupdf` (fitz) to render pages and `Pillow` (PIL) to invert colors.
    *   Replaces page content with the inverted JPEG image.
    *   Optimizes output file size with JPEG compression.
*   **Usage:** `python invert-color-pdf.py <input.pdf> <output.pdf>`

## Multimedia (Audio/Music)

### `auto_tagger.py`
*   **Description:** Automatically adds ID3 tags to MP3 files by looking up metadata on MusicBrainz.
*   **Key Features:**
    *   Walks through a directory to find `.mp3` files.
    *   Guesses Artist/Title from filenames (optimized for Classical music naming conventions).
    *   Queries MusicBrainz API for metadata.
    *   Writes tags (Title, Artist, Album, Date, Composer) using `mutagen`.
*   **Usage:** `python auto_tagger.py <directory_path>`

### `playlist-dowloader.py`
*   **Description:** Downloads audio from a YouTube playlist and converts it to MP3.
*   **Key Features:**
    *   Uses `yt-dlp` for downloading.
    *   Hardcoded playlist URL (Johann Strauss II).
    *   Converts to 320kbps MP3.
*   **Usage:** `python playlist-dowloader.py` (Edit script for URL).

### `spotify-dowloader.py`
*   **Description:** Interactive tool to download Spotify playlists or tracks via YouTube.
*   **Key Features:**
    *   Takes a Spotify URL input.
    *   Fetches metadata from Spotify API (`spotipy`).
    *   Searches for the song on YouTube.
    *   Downloads audio using `pytube` and converts with `moviepy`.
    *   Embeds ID3 tags and Album Art.
    *   Requires `SPOTIPY_CLIENT_ID` and `SPOTIPY_CLIENT_SECRET` environment variables.
*   **Usage:** `python spotify-dowloader.py`

## Data

### `v1-lamica-geniale.txt`
*   **Description:** A text file containing the Italian text of "L'amica geniale" (My Brilliant Friend) by Elena Ferrante.
*   **Context:** This appears to be a source text used for testing the translation or cleaning scripts (or the result of an extraction).
