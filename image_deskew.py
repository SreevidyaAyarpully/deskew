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

    angle_radian = math.radians(angle)
    width = abs(np.sin(angle_radian) * old_height) + abs(np.cos(angle_radian) * old_width)
    height = abs(np.sin(angle_radian) * old_width) + abs(np.cos(angle_radian) * old_height)

    image_center = tuple(np.array(image.shape[1::-1]) / 2)
    rot_mat = cv2.getRotationMatrix2D(image_center, angle, 1.0)
    rot_mat[1, 2] += (width - old_width) / 2
    rot_mat[0, 2] += (height - old_height) / 2
    scale_factor = 1  # Adjust the scaling factor as needed
    return cv2.warpAffine(image, rot_mat, (int(round(height * scale_factor)), int(round(width * scale_factor))))



# Load an image
input_image_path = "input image path"
image = cv2.imread(input_image_path)

# Apply deskewing
deskewed_image = deskew(image)

output_folder = "output folder path"
# Ensure the output folder exists
os.makedirs(output_folder, exist_ok=True)

# Save the deskewed image to the output folder
output_image_path = os.path.join(output_folder, "deskewed_image.jpg")
cv2.imwrite(output_image_path, deskewed_image)
