import os
import wave
from piper import PiperVoice
from piper.config import SynthesisConfig

# === CONFIG ===
INTERFACE_VERSION = "110000, 111002"
MODEL_PATH = "VoiceModels/GB_Female.onnx"
OUTPUT_DIR = os.path.join("../SharedMedia_Unhalted", "Sounds")

# === LOAD PIPER VOICE ===
voice = PiperVoice.load(MODEL_PATH)
syn_config = SynthesisConfig(
    volume=1.0,            # full volume
    length_scale=1.0,      # natural speed
    noise_scale=0.0,       # minimal audio distortion
    noise_w_scale=0.0,     # stable voice tone
    normalize_audio=True   # clean output levels
)


def GenerateTTSFromText(filePath):
    os.makedirs(OUTPUT_DIR, exist_ok=True)
    with open(filePath, 'r') as File:
        for Line in File.read().splitlines():
            Line = Line.strip()
            if not Line:
                continue

            print(f"🔊 Generating TTS for: {Line}")
            sanitized_filename = f"{Line}.wav".replace("/", "_").replace(":", "").replace('"', '')
            output_path = os.path.join(OUTPUT_DIR, sanitized_filename)

            with wave.open(output_path, "wb") as wav_file:
                voice.synthesize_wav(Line, wav_file, syn_config=syn_config)


def CreateAddOn():
    os.makedirs("SharedMedia_Unhalted", exist_ok=True)
    TOCPath = os.path.join("SharedMedia_Unhalted", "SharedMedia_Unhalted.toc")
    LUAPath = os.path.join("SharedMedia_Unhalted", "SharedMedia_Unhalted.lua")

    print("📄 Creating TOC File")
    with open(TOCPath, 'w') as TOCFile:
        TOCFile.write(f'## Interface: {INTERFACE_VERSION}\n')
        TOCFile.write('## Title: SharedMedia - |cFF8080FFUnhalted|r\n')
        TOCFile.write('## Author: Unhalted\n')
        TOCFile.write('## Version: 1.0\n')
        TOCFile.write('SharedMedia_Unhalted.lua\n')

    print("📄 Creating LUA File")
    with open(LUAPath, 'w') as LuaFile:
        LuaFile.write('LSM = LibStub("LibSharedMedia-3.0")\n')
        for File in os.listdir(OUTPUT_DIR):
            if File.endswith(".wav"):
                name = File[:-4].replace('"', '').replace('\\', '')
                LuaFile.write(
                    f'LSM:Register("sound", "|cFF8080FFUnhalted|r: {name}", [[Interface\\AddOns\\SharedMedia_Unhalted\\Sounds\\{File}]])\n'
                )

# === EXECUTION ===
GenerateTTSFromText("../TTS.txt")
# CreateAddOn()
