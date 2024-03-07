import os
import cv2
import math
import numpy as np
from deskew import determine_skew

def deskew(image):
    # Convert the image to grayscale
    gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
    # Calculate the skew
    angle = determine_skew(gray, angle_pm_90=True)
    print(angle)
    # Rotate the image to deskew it
    rotated = rotate_image(image, angle)
    return rotated

def rotate_image(image, angle):
    # Get image dimensions
    old_height, old_width = image.shape[:2]
    # Convert the angle to radians
    angle_radian = math.radians(angle)
    # Calculate the new dimensions of the rotated image
    width = abs(np.sin(angle_radian) * old_height) + abs(np.cos(angle_radian) * old_width)
    height = abs(np.sin(angle_radian) * old_width) + abs(np.cos(angle_radian) * old_height)
    # Calculate the center of the image for rotation
    image_center = tuple(np.array(image.shape[1::-1]) / 2)
    # Create a rotation matrix
    rot_mat = cv2.getRotationMatrix2D(image_center, angle, 1.0)
    # Adjust translation to center the rotated image
    rot_mat[1, 2] += (width - old_width) / 2
    rot_mat[0, 2] += (height - old_height) / 2
    scale_factor = 1  # Adjust the scaling factor as needed
    return cv2.warpAffine(image, rot_mat, (int(round(height * scale_factor)), int(round(width * scale_factor))))


# Input and output folders
input_folder = r"image_deskew\input_image"
output_folder = r"image_deskew\output_image"

# Ensure the output folder exists
os.makedirs(output_folder, exist_ok=True)

# Iterate through all files in the input folder
for filename in os.listdir(input_folder):
    if filename.endswith(('.jpg', '.jpeg', '.png')):  # Add more extensions if needed
        # Construct the full path for the input image
        input_image_path = os.path.join(input_folder, filename)
        # Load the image
        image = cv2.imread(input_image_path)
        # Apply deskewing
        deskewed_image = deskew(image)
        # Construct the output image path with the desired filename
        output_image_filename = f"{os.path.splitext(filename)[0]}_deskew.jpg"
        output_image_path = os.path.join(output_folder, output_image_filename)
        # Save the deskewed image to the output folder
        cv2.imwrite(output_image_path, deskewed_image)
