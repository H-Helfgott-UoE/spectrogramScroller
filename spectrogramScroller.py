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

class ImageSwitcher:
    def __init__(self, root, image_paths, save_dir, saved_list_name):
        self.root = root
        self.image_paths = image_paths
        self.index = 0
        self.is_over = False
        self.image_nb = len(image_paths)
        self.save_dir = save_dir
        self.save_counter = 0
        self.saved_list = []
        self.saved_list_name = saved_list_name

        # Load the first image
        self.image_label = tk.Label(root)
        self.image_label.pack()
        self.load_image(self.index)

        # Bind keypress events to functions
        root.bind("<space>", self.next_image)
        root.bind("<Return>", self.save_image)

    def load_image(self, index):
        img = Image.open(self.image_paths[index])
        self.tk_image = ImageTk.PhotoImage(img)
        self.image_label.config(image=self.tk_image)

    # Go to next image
    def next_image(self, event=None):
        self.index = self.index + 1

        # If images are remaining, keep scrolling
        if self.index < self.image_nb:
            self.load_image(self.index)

        # If no images are left, stay in place and print final message once
        elif not self.is_over:
            print("All files have been visualized")
            print("Saved "+str(self.save_counter)+" files into "+self.save_dir)
            self.is_over = True
            with open(os.path.join(self.save_dir, self.saved_list_name), 'w', newline='') as myfile:
                wr = csv.writer(myfile)
                wr.writerows(zip(self.saved_list))

    # Save image into separate directory, and list
    def save_image(self, event=None):
        new_path = os.path.join(self.save_dir, ntpath.basename(self.image_paths[self.index]))
        if not os.path.isfile(new_path):
            shutil.copyfile(self.image_paths[self.index], new_path)
            self.save_counter += 1
            self.saved_list.append(ntpath.basename(self.image_paths[self.index]))
            print("Image saved")
        else: 
            print("Already saved")

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

    new_file_name = file_path.split(".")[0]+'.png'

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
    # Create spectrogram_directory
    os.mkdir(spectrogram_directory)
    os.mkdir(saved_spectrogram_directory)

    # Parse through audio files
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
    for file_path in tqdm(audio_paths):
        saveSpectrogram(file_path, audio_directory, spectrogram_directory)
    print("Saved "+str(len(audio_paths))+" spectrograms into "+spectrogram_directory)

def startWindow(spectrogram_directory, saved_spectrogram_directory, saved_list_name):
    # Parse through existing spectrograms
    image_paths = []
    for file in os.listdir(spectrogram_directory):
        if file.endswith(".png"):
            image_paths.append(os.path.join(spectrogram_directory, file))

    print("Opened spectrogram window")
    # Launch the window
    app = ImageSwitcher(root, image_paths, saved_spectrogram_directory, saved_list_name)
    root.mainloop()

def main(audio_directory, spectrogram_directory, saved_spectrogram_directory, saved_list_name):
    generateSpectrograms(audio_directory, spectrogram_directory, saved_spectrogram_directory)
    startWindow(spectrogram_directory, saved_spectrogram_directory, saved_list_name)

if __name__ == "__main__":

    #Pre-define app at start (avoids NSException when executed in Mac OS) 
    root = tk.Tk()
    root.title("Press Space to access next image, Return to save image into separate directory")

    main(sys.argv[1], sys.argv[2], sys.argv[3], sys.argv[4])