# Laser Pointer Detection Project

## Overview
This project uses **Python** and **OpenCV** to detect a laser pointer in real-time video and estimate its distance from the camera. Detection is achieved through HSV color thresholding, contour analysis, and distance calculation based on the size of the laser point in the image.

## Features
- **Real-time Laser Detection** using HSV color space.
- **Distance Estimation** using known parameters and focal length calculation.
- **Noise Reduction** through Gaussian Blur and morphological operations.

## Installation
1. Clone the repository:
   ```sh
   git clone https://github.com/username/laser-pointer-detection.git
   cd laser-pointer-detection
   ```

2. Install dependencies:
   ```sh
   pip install -r requirements.txt
   ```

## Usage
Run the script to start detecting the laser pointer:
```sh
python detect.py
```
Press **'q'** to exit.


