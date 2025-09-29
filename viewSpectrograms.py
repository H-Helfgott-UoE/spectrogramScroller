# OS and basic imports
import os
import sys
import ntpath
import shutil
import time
import csv
import pickle

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
    def __init__(self, root, image_paths, spectrogram_dir, save_dir, reviewer, spectrogram_filelist):
        self.root = root
        self.image_paths = image_paths
        self.index = 0

        self.spectrogram_dir = spectrogram_dir
        self.save_dir = save_dir
        self.save_counter = 0
        self.saved_list = []
        self.reviewer = reviewer
        self.reviewed_list = []
        self.spectrogram_filelist = spectrogram_filelist

        # Load the first image
        self.image_label = tk.Label(root)
        self.image_label.pack()
        self.loadImage(self.index)

        # Bind keypress events to functions
        root.bind("<space>", self.nextImage)
        root.bind("<Return>", self.saveImage)
        root.bind("s", self.saveAndLeave)

    # Display image on the window
    def loadImage(self, index):
        img = Image.open(self.image_paths[index])
        self.tk_image = ImageTk.PhotoImage(img)
        self.image_label.config(image=self.tk_image)

    # Go to next image
    def nextImage(self, event=None):
        self.index = self.index + 1
        # If images are remaining, keep scrolling. Otherwise decrement index to avoid count issues in the end-of-session recap
        if self.index < len(self.image_paths):
            self.loadImage(self.index)
        else:
            self.index = self.index - 1

    # Save image into separate directory
    def saveImage(self, event=None):
        new_path = os.path.join(self.save_dir, ntpath.basename(self.image_paths[self.index]))
        if not os.path.isfile(new_path):
            shutil.copyfile(self.image_paths[self.index], new_path)
            self.save_counter += 1
            self.saved_list.append(ntpath.basename(self.image_paths[self.index]))
            print("Image saved")
        else: 
            print("Already saved")

    def saveAndLeave(self, event=None):

        print("======== END OF SESSION ========")

        # Append the names and reviewer of the visualized spectrograms to the appropriate file
        with open(os.path.join(self.spectrogram_dir, "spectrogram_filelist.csv"), 'a', newline='') as myfile:
            wr = csv.writer(myfile)
            for reviewed_file in self.image_paths[:self.index+1]:
                wr.writerow([ntpath.basename(reviewed_file), self.reviewer])

        # Append the names and reviewer of the saved spectrograms to appropriate file
        with open(os.path.join(self.save_dir, "saved_spectrograms.csv"), 'a', newline='') as myfile:
            wr = csv.writer(myfile)
            for saved_filename in self.saved_list:
                wr.writerow([ntpath.basename(saved_filename), self.reviewer])

        print("Reviewed in current session: ",str(self.index+1))
        print("Remaining: ",str(len(self.image_paths)-(self.index+1)))

def startWindow(spectrogram_directory, saved_spectrogram_directory, reviewer_name):

    # Retrieve the existing list of visualized spectrograms
    spectrogram_filelist = []
    with open(os.path.join(spectrogram_directory, 'spectrogram_filelist.csv'), "r") as f:
        reader = csv.reader(f, delimiter="\t")
        for line in reader:
            spectrogram_filelist.append(line)

    # Parse through existing spectrograms, skipping the ones that were already visualized
    unparsed_image_paths = []
    for file in os.listdir(spectrogram_directory):
        if file.endswith(".png") and not any(ntpath.basename(file) in file_tuple[0] for file_tuple in spectrogram_filelist):
            unparsed_image_paths.append(os.path.join(spectrogram_directory, file))

    print("======== START OF SESSION ========")
    print("Total number of spectrograms: ",str(len(unparsed_image_paths)+len(spectrogram_filelist)))
    print("Already verified: ",str(len(spectrogram_filelist)))
    print("Remaining: ",str(len(unparsed_image_paths)))

    if len(unparsed_image_paths) == 0:
        print("All files have been reviewed")
        print("======== END OF SESSION ========")
    else:
        print("Opening spectrogram window")
        # Launch the window
        app = ImageSwitcher(root, unparsed_image_paths, spectrogram_directory, saved_spectrogram_directory, reviewer_name, spectrogram_filelist)
        root.mainloop()

def main(spectrogram_directory, saved_spectrogram_directory, reviewer_name):
    startWindow(spectrogram_directory, saved_spectrogram_directory, reviewer_name)

if __name__ == "__main__":

    #Pre-define app at start (avoids NSException when executed in Mac OS) 
    root = tk.Tk()
    root.title("Space = Next Image | Return = Save Image | s = Save Progress and Leave")

    main(sys.argv[1], sys.argv[2], sys.argv[3])