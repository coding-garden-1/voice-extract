import os
from pydub import AudioSegment
import time
import shutil

cwd = os.getcwd()

print(cwd)

timestamp = time.time()

shutil.move("labels.txt", os.path.join("output", "labels.txt"))

shutil.move("video.mp3", os.path.join("output", "video.mp3"))

os.chdir("output")

outputfolder = f"output_{timestamp}"

os.mkdir(outputfolder)

shutil.move("labels.txt", os.path.join(outputfolder, "labels.txt"))
shutil.move("video.mp3", os.path.join(outputfolder, "video.mp3"))

os.chdir(outputfolder)

# Function to extract audio segments from the mp3 file based on timestamps
def extract_audio(input_file, output_file, start_time, end_time):
    audio = AudioSegment.from_file(input_file)
    extracted_audio = audio[start_time * 1000: end_time * 1000]  # Extract audio based on start and end timestamps
    extracted_audio.export(output_file, format="mp3")  # Export the extracted audio to mp3 format
    return extracted_audio

# Read the labels.txt file and extract audio segments for each speaker
speaker_files = {}

with open("labels.txt", "r") as file:
    lines = file.readlines()
    for line in lines:
        # Get the speaker ID and start/end timestamps from each line
        start_time, end_time, speaker = line.split("\t")
        output_filename = f"{speaker}_{start_time}_{end_time}.mp3"
        
        if speaker not in speaker_files:
            speaker_files[speaker] = []
        
        audio = extract_audio("video.mp3", output_filename, float(start_time), float(end_time))
        speaker_files[speaker].append(audio)

# Concatenate audio segments for each speaker
for speaker, audio_segments in speaker_files.items():
    concatenated_audio = AudioSegment.empty()
    for audio in audio_segments:
        concatenated_audio += audio
    
    concatenated_audio.export(f"{speaker}_concatenated.mp3", format="mp3")

# Clean up
files_to_keep = ["video.mp3"] + [f"{speaker}_concatenated.mp3" for speaker in speaker_files.keys()]

for file in os.listdir(os.getcwd()):
    if file.endswith(".mp3") and file not in files_to_keep:
        os.remove(file)
