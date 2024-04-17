# NCGR Script Documentation

## Overview

This script processes a folder of WAV files containing recorded calls. It loops through each WAV file, saves the file path in a dictionary, sends each file to the Speechlog analytics API for transcription, receives the transcribed text, and saves it in a JSON file.

![Beige Colorful Minimal Flowchart Infographic Graph](https://github.com/Ibrahimnalmanaseer/curl/assets/62019258/15b12a8d-34a6-4666-bfc1-080f181e8593)


## Steps

1. **Loop Through WAV Files**:
   - Access the folder containing WAV files.
   - Iterate through each WAV file in the folder.

2. **Save File Path in Dictionary**:
   - Save the full path of each WAV file in a dictionary.

3. **Send File to API**:
   - Send each WAV file to the API endpoint for transcription.
   - Use the saved dictionary to track file paths.

4. **Receive Text Response**:
   - Receive the transcribed text response from the API for each file.

5. **Save Text in JSON File**:
   - Save the transcribed text in a JSON file.
  

## Script Specifications

- Input: Folder path containing WAV files.
- Output: JSON files containing transcribed text for each WAV file.


