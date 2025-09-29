# Spectrogram Scroller #

This snipper creates a pop-up window where one can examine spectrograms one after another, and save them into a separate directory if needed

# How to use #

## STEP 1 ##

Run the following command to generate all spectrograms at once
```
python3 generateSpectrograms.py audio_dir spect_dir saved_dir
```
**Arguments**
- audio_dir: EXISTING directory of audio .wav files to visualize
- spect_dir: directory TO BE CREATED by the code, will contain all spectrograms
- saved_dir: directory TO BE CREATED by the code, will contain the spectrograms saved as "interesting" during step 2

Both relative and absolute paths are supported

## STEP 2 ##

Run the following command to start visualizing spectrograms
```
python3 viewSpectrograms.py spect_dir saved_dir reviewer
```
**Arguments**
- spect_dir: EXISTING directory containing all spectrograms, must be the same one created in step 1
- saved_dir: EXISTING directory for saved spectrograms, must be the same one created in step 1
- reviewer: String indicating the name of the reviewer

Both relative and absolute paths are supported

**Annotation Process**
- Once the command is validated, a pop-up window will appear with a spectrogram
- Press Space to advance to next spectrogram, Return to save the spectrogram in saved_dir
- When done, press s to save your progress and exit. Once the end-of-session report is printed in the command line, you may close the pop-up

Repeat this step as many times as needed to annotate all files. The code will **locally** keep track of which spectrograms you have already viewed, and will never show the same spectrogram twice. At the beginning and end of each session, you will see how many spectrograms were viewed and how much are remaining.

If you want to review all spectrograms regardless of whether they were seen before (e.g. if they were seen by another reviewer who you suspect may be sabotaging your project), erasing the contents of spect_dir/spectrogram_filelist.csv will reinitialize viewing information and allow you to do so. It is recommended to keep a separate copy of the file before erasing its contents.

If you add spectrograms in spect_dir/ between two sessions, they will be taken into account in all future sessions.

# Requirements #

Python >=3.9

Libraries:
- numpy
- matplotlib
- tqdm
- pillow
- soundfile
- scipy
