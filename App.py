import pyttsx3
import os

TTSEngine = pyttsx3.init()
TTSEngine.setProperty('rate', 200)
TTSEngine.setProperty('volume', 1.0)

def GenerateTTSFromText(filePath):
    OutputDirectory = os.path.join('SharedMedia_Unhalted', 'Sounds')
    os.makedirs(OutputDirectory, exist_ok=True)
    with open(filePath, 'r') as File:
        TextToRead = File.read().splitlines()
        
        for Line in TextToRead:
            OutputPath = os.path.join(OutputDirectory, f"{Line}.mp3")
            TTSEngine.save_to_file(Line, OutputPath)
            print("Generating MP3: ", Line)
            TTSEngine.runAndWait()

def CreateAddOn():
    # Ensure the main directory exists
    os.makedirs('SharedMedia_Unhalted', exist_ok=True)
    TOCPath = os.path.join('SharedMedia_Unhalted', 'SharedMedia_Unhalted.toc')
    LUAPath = os.path.join('SharedMedia_Unhalted', 'SharedMedia_Unhalted.lua')
    with open(TOCPath, 'w') as TOCFile:
        TOCFile.write('## Interface: 110000, 110002\n')
        TOCFile.write('## Title: SharedMedia - |cFF8080FFUnhalted|r\n')
        TOCFile.write('## Author: Unhalted\n')
        TOCFile.write('## Version: 1.0\n')
        TOCFile.write('SharedMedia_Unhalted.lua\n')
    with open(LUAPath, 'w') as LuaFile:
        LuaFile.write('LSM = LibStub("LibSharedMedia-3.0")\n')
        sounds_dir = os.path.join('SharedMedia_Unhalted', 'Sounds')
        for File in os.listdir(sounds_dir):
            if File.endswith('.mp3'):
                LuaFile.write(f'LSM:Register("sound", "|cFF8080FFUnhalted|r: {File[:-4]}", [[Interface\AddOns\SharedMedia_Unhalted\Sounds\{File}]])\n')

GenerateTTSFromText('TTS.txt')
CreateAddOn()
