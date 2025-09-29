# OS and basic imports
import os
import sys
import ntpath
import shutil
import time
import csv

# Math & Display imports
import numpy as np
import matplotlib.pyplot as plt
from tqdm import tqdm

# Audio processing imports
import tkinter as tk
from PIL import Image, ImageTk
import soundfile as sf
from scipy.signal import spectrogram

def saveSpectrogram(file_path, audio_directory, spectrogram_directory):

    # Open given file
    data, samplerate = sf.read(os.path.join(audio_directory, file_path))

    nperseg = 2048
    noverlap = nperseg // 2
    frequencies, times, Sxx = spectrogram(data, fs=samplerate, nperseg=nperseg, noverlap=noverlap)

    # Convert power into decibels
    Sxx_dB = 10 * np.log10(Sxx + 1e-10)

    # Prevent matplotlib display
    plt.ioff()

    new_file_name = ntpath.basename(file_path).split(".")[0]+'.png'

    # Save spectrogram as png file
    plt.figure(figsize=(12, 6))
    plt.pcolormesh(times, frequencies, Sxx_dB, shading='gouraud')
    plt.ylabel('Frequency [Hz]')
    plt.xlabel('Time [sec]')
    plt.title('File: '+file_path)
    plt.colorbar(label='Intensity [dB]')
    plt.ylim(0, samplerate/2)
    plt.savefig(os.path.join(spectrogram_directory, new_file_name))
    plt.close()

def generateSpectrograms(audio_directory, spectrogram_directory, saved_spectrogram_directory):

    # Create directories for spectrograms and saved examples
    os.mkdir(spectrogram_directory)
    os.mkdir(saved_spectrogram_directory)

    # Parse through audio files in given directory
    print("Parsing through audio files in "+audio_directory)
    audio_paths = []
    for file in os.listdir(audio_directory):
        if file.endswith(".wav"):
            audio_paths.append(file)
    if len(audio_paths) == 0:
        print("Error: No audio files found")
        exit()

    print("Number of audio files found: "+str(len(audio_paths)))
    time.sleep(0.5)

    # Generating spectrograms
    print("Generating spectrograms")

    # Save all spectrograms
    for file_path in tqdm(audio_paths):
        saveSpectrogram(file_path, audio_directory, spectrogram_directory)
    
    # Create the spectrogram book-keeping file
    with open(os.path.join(spectrogram_directory, 'spectrogram_filelist.csv'), 'w') as file:
        pass

    print("Saved "+str(len(audio_paths))+" spectrograms into "+spectrogram_directory)

def main(audio_directory, spectrogram_directory, saved_spectrogram_directory):
    generateSpectrograms(audio_directory, spectrogram_directory, saved_spectrogram_directory)

if __name__ == "__main__":
    main(sys.argv[1], sys.argv[2], sys.argv[3])