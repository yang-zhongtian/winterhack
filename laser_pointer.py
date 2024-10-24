"""
Laser Pointer Distance Measurement
This script detects a red laser pointer dot in a video stream and calculates the distance to the laser pointer based on its size.

Author: Zhongtian Yang
Date: 2024-10-24
"""

import sys
import cv2
import numpy as np

# Define known distance (in meters) and size of the laser dot (in pixels)
KNOWN_DISTANCE = 2.0  # meters
KNOWN_RADIUS = 3  # pixels
TOLERANCE = 0.1  # meters (10 cm tolerance)

# Color detection range for red laser in HSV space (adjust as needed for different colors)
lower_red1 = np.array([0, 100, 160])  # Lower range for red color
upper_red1 = np.array([10, 255, 255])  # Upper range for red color

lower_red2 = np.array([160, 100, 160])  # Lower range for red color
upper_red2 = np.array([180, 255, 255])  # Upper range for red color


def detect_laser(image: np.ndarray) -> tuple[np.ndarray, float | None]:
    """
    Detect the laser pointer in the image and calculate the distance to it.
    If no laser pointer is detected, return None for distance.

    :param image: Input image containing a red laser pointer dot
    :return: Tuple containing the output image with the detected laser dot and the calculated distance (in meters)
    """
    # Convert the image to HSV color space
    hsv_image = cv2.cvtColor(image, cv2.COLOR_BGR2HSV)

    # Mask for red color
    red_mask1 = cv2.inRange(hsv_image, lower_red1, upper_red1)
    red_mask2 = cv2.inRange(hsv_image, lower_red2, upper_red2)

    # Combine the two red masks
    red_mask = cv2.bitwise_or(red_mask1, red_mask2)

    # Apply morphological operations: first dilate, then erode
    dilate_kernel = np.ones((4, 4), np.uint8)
    dilated_mask = cv2.dilate(red_mask, dilate_kernel, iterations=2)  # Dilation
    erode_kernel = np.ones((5, 5), np.uint8)
    eroded_mask = cv2.erode(dilated_mask, erode_kernel, iterations=8)  # Erosion

    # Find contours of the laser dot
    contours, _ = cv2.findContours(eroded_mask, cv2.RETR_TREE, cv2.CHAIN_APPROX_SIMPLE)

    # Proceed if at least one contour is found
    if contours:
        # Assume the largest contour is the laser dot
        largest_contour = max(contours, key=cv2.contourArea)
        (x, y), radius = cv2.minEnclosingCircle(largest_contour)

        # Only consider if the radius is significant (to avoid noise)
        if radius > 1:
            # Draw the detected laser dot
            cv2.circle(image, (int(x), int(y)), int(radius), (0, 255, 0), 2)

            # Calculate the distance based on dot size
            distance = (KNOWN_RADIUS / radius) * KNOWN_DISTANCE

            return image, distance

    return image, None


def main():
    # Open video capture (0 for the default camera, or replace with video file path)
    cap = cv2.VideoCapture(0)

    if not cap.isOpened():
        print("Error: Could not open video.")
        sys.exit(1)

    while True:
        # Read a frame from the video
        ret, frame = cap.read()

        # If the frame was not successfully captured, break the loop
        if not ret:
            print("Error: Failed to capture frame.")
            break

        # Detect the laser pointer and calculate distance
        frame, distance = detect_laser(frame)

        # Display the results
        if distance:
            cv2.putText(frame, f"Distance: {distance:.2f} meters", (50, 50), cv2.FONT_HERSHEY_SIMPLEX,
                        1, (255, 255, 255), 2)

            # Check if the distance is within tolerance
            if KNOWN_DISTANCE - TOLERANCE <= distance <= KNOWN_DISTANCE + TOLERANCE:
                cv2.putText(frame, "Within Range", (50, 100), cv2.FONT_HERSHEY_SIMPLEX,
                            1, (0, 255, 0), 2)
            else:
                cv2.putText(frame, "Out of Range", (50, 100), cv2.FONT_HERSHEY_SIMPLEX,
                            1, (0, 0, 255), 2)

        # Display the image
        cv2.imshow('Laser Detection', frame)

        # Wait for a key press; exit on 'q'
        if cv2.waitKey(1) & 0xFF == ord('q'):
            break

    # Release the video capture and close all OpenCV windows
    cap.release()
    cv2.destroyAllWindows()


if __name__ == "__main__":
    main()
