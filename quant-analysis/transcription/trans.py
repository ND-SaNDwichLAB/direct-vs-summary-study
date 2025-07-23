import os
import openai

openai.api_key = os.environ.get("OPENAI_API_KEY")

filename = "your-filename"

with open(f"audio/{filename}.m4a", "rb") as audio_file:
    transcript = openai.audio.transcriptions.create(model="whisper-1", file=audio_file)
print(transcript)

transcript_text = transcript.text.replace(" ", "\n")
with open(f"transcript/{filename}.txt", "w", encoding="utf-8") as text_file:
    text_file.write(transcript_text)
