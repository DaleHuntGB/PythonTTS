import pyttsx3
import os

# Global
INTERFACE_VERSION = "110000, 111002"

# Init TTS Engine
TTSEngine = pyttsx3.init()
TTSEngine.setProperty('rate', 200) # Rate of Speech
TTSEngine.setProperty('volume', 1.0)

def GenerateTTSFromText(filePath):
    OutputDirectory = os.path.join('SharedMedia_Unhalted', 'Sounds') # Define Output Directory
    os.makedirs(OutputDirectory, exist_ok=True)
    with open(filePath, 'r') as File:
        TextToRead = File.read().splitlines() # Read Text File        
        for Line in TextToRead:
            OutputPath = os.path.join(OutputDirectory, f"{Line}.mp3")
            TTSEngine.save_to_file(Line, OutputPath) # Save Each Read TTS to MP3
            TTSEngine.runAndWait()

def CreateAddOn():
    os.makedirs('SharedMedia_Unhalted', exist_ok=True)
    TOCPath = os.path.join('SharedMedia_Unhalted', 'SharedMedia_Unhalted.toc')
    LUAPath = os.path.join('SharedMedia_Unhalted', 'SharedMedia_Unhalted.lua')
    with open(TOCPath, 'w') as TOCFile: # Write TOC File with Relevant Information
        TOCFile.write(f'## Interface: {INTERFACE_VERSION}\n')
        TOCFile.write('## Title: SharedMedia - |cFF8080FFUnhalted|r\n')
        TOCFile.write('## Author: Unhalted\n')
        TOCFile.write('## Version: 1.0\n')
        TOCFile.write('SharedMedia_Unhalted.lua\n')
    with open(LUAPath, 'w') as LuaFile:
        LuaFile.write('LSM = LibStub("LibSharedMedia-3.0")\n')
        SoundsDirectory = os.path.join('SharedMedia_Unhalted', 'Sounds')
        for File in os.listdir(SoundsDirectory):
            if File.endswith('.mp3'):
                LuaFile.write(f'LSM:Register("sound", "|cFF8080FFUnhalted|r: {File[:-4]}", [[Interface\AddOns\SharedMedia_Unhalted\Sounds\{File}]])\n') # Register Each Sound with LSM

GenerateTTSFromText('TTS.txt')
CreateAddOn()