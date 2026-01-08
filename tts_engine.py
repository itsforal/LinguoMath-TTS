import re
import os
import asyncio
import logging
from typing import List, Tuple
from edge_tts import Communicate
from pydub import AudioSegment
from pylatexenc.latex2text import LatexNodes2Text

# Setup Logging
logging.basicConfig(level=logging.INFO, format='%(levelname)s: %(message)s')

class LinguoMathEngine:
    """
    A professional engine to convert multi-lingual (Farsi/English) 
    Markdown & LaTeX text into high-quality speech.
    """
    
    def __init__(self, voice_fa="fa-IR-DilaraNeural", voice_en="en-US-JennyNeural"):
        self.voice_fa = voice_fa
        self.voice_en = voice_en
        self.latex_converter = LatexNodes2Text()

    def clean_text(self, text: str) -> str:
        """Removes Markdown syntax and formats math symbols."""
        # Strip Markdown symbols
        text = re.sub(r'#+\s?', '', text)
        text = re.sub(r'(\*\*|__)(.*?)\1', r'\2', text)
        text = re.sub(r'(\*|_)(.*?)\1', r'\2', text)
        text = re.sub(r'---', ' ', text)
        
        # Advanced LaTeX to Text mapping
        math_map = {
            r'\\rightarrow': ' leads to ',
            r'\\leftarrow': ' comes from ',
            r'\\sum': ' summation of ',
            r'\\frac\{(.+?)\}\{(.+?)\}': r' \1 divided by \2 ',
            r'\\sqrt\{(.+?)\}': r' square root of \1 ',
            r'\^2': ' squared ',
            r'\\mu': ' mew ',
            r'\\sigma': ' sigma ',
            r'\\beta': ' beta ',
            r'\\epsilon': ' epsilon ',
        }
        
        for pattern, replacement in math_map.items():
            text = re.sub(pattern, replacement, text)
            
        # Standardize math delimiters
        text = re.sub(r'\$\$?(.+?)\$\$?', r' \1 ', text)
        return text

    def detect_voice(self, text: str) -> str:
        """Determines if the voice should be Persian or English."""
        farsi_chars = len(re.findall(r'[\u0600-\u06FF]', text))
        english_chars = len(re.findall(r'[a-zA-Z]', text))
        return self.voice_fa if farsi_chars >= english_chars else self.voice_en

    async def generate_chunk(self, text: str, index: int) -> str:
        """Synthesizes a single text segment into an MP3 file."""
        voice = self.detect_voice(text)
        filename = f"temp_{index}.mp3"
        try:
            communicate = Communicate(text, voice)
            await communicate.save(filename)
            return filename
        except Exception as e:
            logging.error(f"Failed chunk {index}: {e}")
            return ""

    async def process_full_text(self, text: str, output_path: str):
        """Main pipeline: Split, Synthesize (Concurrent), and Merge."""
        # 1. Split into meaningful sentences/lines
        lines = [line.strip() for line in text.split('\n') if line.strip()]
        cleaned_lines = [self.clean_text(line) for line in lines]

        logging.info(f"Processing {len(cleaned_lines)} segments...")

        # 2. Concurrent Processing (Fast!)
        tasks = [self.generate_chunk(line, i) for i, line in enumerate(cleaned_lines)]
        temp_files = await asyncio.gather(*tasks)
        temp_files = [f for f in temp_files if f] # Filter empty results

        # 3. Merge Audio
        logging.info("Stitching audio segments...")
        final_audio = AudioSegment.empty()
        for file in temp_files:
            segment = AudioSegment.from_mp3(file)
            final_audio += segment + AudioSegment.silent(duration=300)
            os.remove(file) # Clean up temp files immediately

        final_audio.export(output_path, format="mp3")
        logging.info(f"Successfully created: {output_path}")