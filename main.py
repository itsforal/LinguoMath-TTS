import asyncio
import argparse
from tts_engine import LinguoMathEngine

async def run_cli():
    parser = argparse.ArgumentParser(description="LinguoMath TTS: Professional Markdown & Math to Speech")
    parser.add_argument("-i", "--input", required=True, help="Input .txt or .md file path")
    parser.add_argument("-o", "--output", default="output.mp3", help="Output audio path")
    parser.add_argument("--voice-fa", default="fa-IR-DilaraNeural", help="Persian voice")
    parser.add_argument("--voice-en", default="en-US-JennyNeural", help="English voice")

    args = parser.parse_args()

    try:
        with open(args.input, 'r', encoding='utf-8') as f:
            content = f.read()
    except FileNotFoundError:
        print(f"Error: File {args.input} not found.")
        return

    engine = LinguoMathEngine(voice_fa=args.voice_fa, voice_en=args.voice_en)
    await engine.process_full_text(content, args.output)

if __name__ == "__main__":
    asyncio.run(run_cli())