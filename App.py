import os
from elevenlabs import ElevenLabs

# === CONFIG ===
INTERFACE_VERSION = "110000, 111002"
API_KEY = os.getenv("ELEVEN_LABS_TTS")
VOICE_ID = "cgSgspJ2msm6clMCkdW9" # Jessica
MODEL_ID = "eleven_monolingual_v1"
OUTPUT_DIR = os.path.join("SharedMedia_Unhalted", "Sounds")

def ListAllVoices():
    print("🔍 Listing all available voices:")
    resp = client.voices.search(search="", page_size=100, include_total_count=False)
    for voice in resp.voices:
        print(f"- {voice.name} (ID: {voice.voice_id}, Category: {voice.category})")

# === INIT CLIENT ===
client = ElevenLabs(api_key=API_KEY)

def GenerateTTSFromText(filePath):
    os.makedirs(OUTPUT_DIR, exist_ok=True)
    with open(filePath, 'r') as File:
        for Line in File.read().splitlines():
            Line = Line.strip()
            if not Line:
                continue

            print(f"Generating TTS for: {Line}")
            audio = client.text_to_speech.convert(
                text=Line,
                voice_id=VOICE_ID,
                model_id=MODEL_ID,
                output_format="mp3_44100_128",
                voice_settings= {
                    "stability": 1.00,
                    "similarity_boost": 1.00,
                }
            )

            sanitized_filename = f"{Line}.mp3".replace("/", "_").replace(":", "").replace('"', '')
            output_path = os.path.join(OUTPUT_DIR, sanitized_filename)
            with open(output_path, "wb") as f:
                for chunk in audio:
                    f.write(chunk)


def CreateAddOn():
    os.makedirs("SharedMedia_Unhalted", exist_ok=True)
    TOCPath = os.path.join("SharedMedia_Unhalted", "SharedMedia_Unhalted.toc")
    LUAPath = os.path.join("SharedMedia_Unhalted", "SharedMedia_Unhalted.lua")

    print("Creating TOC File")
    with open(TOCPath, 'w') as TOCFile:
        TOCFile.write(f'## Interface: {INTERFACE_VERSION}\n')
        TOCFile.write('## Title: SharedMedia - |cFF8080FFUnhalted|r\n')
        TOCFile.write('## Author: Unhalted\n')
        TOCFile.write('## Version: 1.0\n')
        TOCFile.write('SharedMedia_Unhalted.lua\n')

    print("Creating LUA File")
    with open(LUAPath, 'w') as LuaFile:
        LuaFile.write('LSM = LibStub("LibSharedMedia-3.0")\n')
        for File in os.listdir(OUTPUT_DIR):
            if File.endswith(".mp3"):
                name = File[:-4].replace('"', '').replace('\\', '')
                LuaFile.write(
                    f'LSM:Register("sound", "|cFF8080FFUnhalted|r: {name}", [[Interface\\AddOns\\SharedMedia_Unhalted\\Sounds\\{File}]])\n'
                )

# === EXECUTION ===
GenerateTTSFromText("TTS.txt")
# CreateAddOn()
