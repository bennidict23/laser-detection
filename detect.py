import cv2
import numpy as np

# Constants for known parameters
KNOWN_DISTANCE = 50.0  # Known distance from the camera to the object in centimeters
KNOWN_WIDTH = 0.5      # Actual width of the laser point in centimeters (adjust based on measurement)

# Function to calculate the focal length of the camera
def calculate_focal_length(known_distance, known_width, width_in_image):
    focal_length = (width_in_image * known_distance) / known_width
    return focal_length

# Function to calculate the distance from the camera to the object
def calculate_distance(focal_length, known_width, width_in_image):
    if width_in_image == 0:
        return None
    distance = (known_width * focal_length) / width_in_image
    return distance

# Initialize the webcam
cap = cv2.VideoCapture(0)

# Check if the webcam is opened correctly
if not cap.isOpened():
    print("Cannot open webcam")
    exit()

# Initialize focal length variable
focal_lengths = []

# Define the HSV color range for detecting the laser pointer (adjust based on actual laser color)
# Red color ranges in HSV
lower_red_1 = np.array([0, 150, 150])
upper_red_1 = np.array([10, 255, 255])
lower_red_2 = np.array([170, 150, 150])
upper_red_2 = np.array([180, 255, 255])

while True:
    # Capture frame-by-frame
    ret, frame = cap.read()
    if not ret:
        print("Cannot receive frame. Exiting...")
        break

    # Convert the frame to HSV color space
    hsv = cv2.cvtColor(frame, cv2.COLOR_BGR2HSV)

    # Apply Gaussian Blur to reduce noise
    blurred = cv2.GaussianBlur(hsv, (5, 5), 0)

    # Create masks for the red color
    mask1 = cv2.inRange(blurred, lower_red_1, upper_red_1)
    mask2 = cv2.inRange(blurred, lower_red_2, upper_red_2)
    mask = cv2.bitwise_or(mask1, mask2)

    # Morphological operations to remove noise
    kernel = np.ones((3, 3), np.uint8)
    mask = cv2.erode(mask, kernel, iterations=2)
    mask = cv2.dilate(mask, kernel, iterations=2)

    # Find contours in the mask
    contours, _ = cv2.findContours(mask, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)

    # Loop over the contours
    for cnt in contours:
        area = cv2.contourArea(cnt)
        if area > 50:  # Filter out small contours
            perimeter = cv2.arcLength(cnt, True)
            if perimeter == 0:
                continue
            # Calculate circularity to check if the contour is circular (laser point)
            circularity = 4 * np.pi * (area / (perimeter * perimeter))
            if circularity > 0.7:
                # Get the bounding rectangle of the contour
                x, y, w, h = cv2.boundingRect(cnt)
                aspect_ratio = float(w) / h
                if 0.8 < aspect_ratio < 1.2:
                    # Draw the bounding rectangle around the detected laser point
                    cv2.rectangle(frame, (x, y), (x + w, y + h), (0, 255, 0), 2)
                    laser_width_in_image = w

                    if len(focal_lengths) < 5:
                        # Calculate the focal length using the known distance and width, collect multiple samples
                        focal_lengths.append(calculate_focal_length(KNOWN_DISTANCE, KNOWN_WIDTH, laser_width_in_image))
                        if len(focal_lengths) == 5:
                            focal_length = np.mean(focal_lengths)
                            print(f"Focal length calculated: {focal_length}")
                    elif len(focal_lengths) >= 5:
                        # Calculate the distance from the camera to the laser point
                        focal_length = np.mean(focal_lengths)
                        distance = calculate_distance(focal_length, KNOWN_WIDTH, laser_width_in_image)
                        if distance is not None:
                            # Display the distance on the frame
                            cv2.putText(frame, f"Distance: {distance:.2f} cm", (x, y - 10),
                                        cv2.FONT_HERSHEY_SIMPLEX, 0.6, (0, 255, 0), 2)
                            # Check if the distance is within the tolerance range
                            if 190 <= distance <= 210:
                                cv2.putText(frame, "Within tolerance", (x, y - 30),
                                            cv2.FONT_HERSHEY_SIMPLEX, 0.6, (255, 0, 0), 2)
                    break  # Process only the first detected laser point

    # Display the resulting frame
    cv2.imshow('Laser Pointer Detection', frame)

    # Press 'q' to exit the loop
    if cv2.waitKey(1) & 0xFF == ord('q'):
        break

# Release the webcam and close windows
cap.release()
cv2.destroyAllWindows()
