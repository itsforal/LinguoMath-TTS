# LinguoMath TTS 🎙️

A custom-built Text-to-Speech (TTS) pipeline designed to convert complex **Markdown** documents and **LaTeX Mathematics** into high-quality audio. This tool is specifically optimized for bilingual content (**Persian & English**).

##  Key Features
- **Smart Voice Switching:** Automatically detects language at the sentence level to switch between Persian (Dilara) and English (Jenny) voices.
- **LaTeX Math Support:** Intelligently verbalizes mathematical formulas (fractions, sums, Greek letters) into natural English speech.
- **Asynchronous Pipeline:** Uses `asyncio` to synthesize audio segments in parallel, significantly reducing processing time.
- **Markdown Friendly:** Automatically cleans headers, bold text, and lists for a seamless listening experience.

##  Installation

1. **Prerequisites:** 
   - Python 3.8+
   - **FFmpeg** (Required for audio merging). 
     - *Mac:* `brew install ffmpeg`
     - *Linux:* `sudo apt install ffmpeg`

2. **Clone & Install:**
   ```bash
   git clone https://github.com/yourusername/LinguoMath-TTS.git
   cd LinguoMath-TTS
   pip install -r requirements.txt
