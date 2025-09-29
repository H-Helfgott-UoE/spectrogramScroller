## Spectrogram Scroller ##

This snipper creates a pop-up window where one can examine spectrograms one after another, and save them into a separate directory if needed

## How to Use ##

**spectrogramScroller.ipynb:**

- Edit cell 2 to replace the existing paths with your own. audio_directory MUST already exist upon call, spectrogram_directory and saved_spectrogram_directory CANNOT exist and will be created by the code.
- Run cells one after another, the last one will open the reviewing window.
- When pressing Space does not change the image anymore, it means that all images have been parsed. You can simply close the window.

**spectrogramScroller.py:**

You can run the script by entering the following command into a terminal (in the same directory as the script) with your own arguments:
```
python3 spectrogramScroller.py audio_directory spectrogram_directory saved_spectrogram_directory saved_list_name
```

Where audio_directory is an EXISTING directory containing the audio .wav files, spectrogram_directory and saved_spectrogram_directory directory names to be CREATED by the code, and saved_list_name the name of a csv file to be CREATED by the code, which will contain a list of all the spectrograms selected by the reviewer

Upon running the code, the reviewing window will display on its own. When pressing Space does not change the image anymore, it means that all images have been parsed. You can simply close the window.

## Requirements ##

Python >=3.9

Libraries:
- numpy
- matplotlib
- tqdm
- pillow
- soundfile
- scipy
