# Laser Pointer Distance Calculator

Author: Zhongtian Yang

This Python script is designed to detect a red laser pointer dot in a video stream and calculate the distance to the
laser pointer based on its size. It uses the OpenCV library for image processing and analysis.

## Code Repository

**https://github.com/yang-zhongtian/winterhack**

## Overview

The script processes video input from a camera (or a video file) to detect the position of a red laser dot. The distance
to the laser is calculated using the known size of the laser dot. The detection is based on color filtering in the HSV
color space and utilizes contour detection techniques.

## Requirements

To run this script, ensure you have the following installed:

- Python 3.x
- OpenCV
- NumPy

You can install the necessary libraries using pip:

```bash
pip install opencv-python numpy
```

## Constants

### Distance and Shape Parameters

```python
KNOWN_DISTANCE = 2.0  # meters
KNOWN_RADIUS = 3  # pixels
TOLERANCE = 0.1  # meters (10 cm tolerance)
```

- `KNOWN_DISTANCE`: The distance to the laser pointer when the radius of the laser dot is known.
- `KNOWN_RADIUS`: The expected radius of the laser dot in pixels.
- `TOLERANCE`: Acceptable margin of error for distance measurement.

### Color Ranges

```python
lower_red1 = np.array([0, 100, 160])  # Lower range for red color
upper_red1 = np.array([10, 255, 255])  # Upper range for red color

lower_red2 = np.array([160, 100, 160])  # Lower range for red color
upper_red2 = np.array([180, 255, 255])  # Upper range for red color
```

These arrays define the HSV color ranges for detecting red colors. Since red can appear in two segments of the HSV color
space, we specify two ranges.

## Core Ideas

The following flow diagram illustrates the process of detecting the laser pointer:

```mermaid
flowchart TD
    A[Start] --> B[Read Frame from Video]
    B --> C[Convert to HSV & Apply Red Mask]
    C --> D[Apply Morphological Operations]
    D --> E{Find Contours?}
    E -- Yes --> F[Find Largest Contour and Calculate Distance]
    F --> G[Draw Dot and Distance on Frame]
    E -- No --> H[Return Frame with No Distance]
    G --> I[Display Frame]
    H --> I
    I --> J{Is 'q' Pressed?}
    J -- Yes --> K[End]
    J -- No --> B
```

## The methods to extract the laser dot

### 1. Color Filtering

1. Convert the frame to the HSV color space.
2. Mask the red color in the frame using the specified color ranges.

<img src="doc/color_filter.png" alt="Color Filtered Image" style="zoom: 33%;" />

### 2. Dilate

Dilate the mask to fill in the center of the laser dot, which is white and neglected in the color filtering step.

<img src="doc/dilate.png" alt="Dilated Image" style="zoom: 33%;" />

### 3. Erode

Erode the mask to remove the surrounding red light beam and keep only the laser dot in the center.

<img src="doc/erode.png" alt="Eroded Image" style="zoom: 33%;" />

### 4. Contour Detection

Find the dot radius and position by matching the image with circle contours.

<img src="doc/contour.png" alt="Contour Detection" style="zoom: 33%;" />

### 5. Distance Calculation

Calculate the distance to the laser pointer based on the known size of the laser dot.

The formula used for distance calculation is:

$ distance = \frac{KnownRadius * KnownDistance}{radius} $

<img src="doc/distance.png" alt="Distance Calculation" style="zoom: 33%;" />