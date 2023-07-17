import cv2
import numpy as np
import pandas as pd
import argparse

# Creating argument parser to take image path from command line
ap = argparse.ArgumentParser()
ap.add_argument('-i', '--image', required=True, help="Image Path")
args = vars(ap.parse_args())
image_path = args['image']

# Read the image with OpenCV
image = cv2.imread(image_path)

# Set the fixed window size
window_width = 800
window_height = 600

# Resize the image if its size exceeds the window size
image_height, image_width, _ = image.shape
if image_width > window_width or image_height > window_height:
    scale = min(window_width / image_width, window_height / image_height)
    new_width = int(image_width * scale)
    new_height = int(image_height * scale)
    image = cv2.resize(image, (new_width, new_height))

# Declare global variables (to be used later)
is_clicked = False
red = green = blue = x_pos = y_pos = 0

# Read CSV file with pandas and assign names to each column
columns = ["color", "color_name", "hex", "R", "G", "B"]
color_data = pd.read_csv('colors.csv', names=columns, header=None)

# Function to calculate the minimum distance from all colors and find the closest matching color
def get_color_name(R, G, B):
    min_distance = 10000
    closest_color_name = ""
    for i in range(len(color_data)):
        distance = abs(R - int(color_data.loc[i, "R"])) + abs(G - int(color_data.loc[i, "G"])) + abs(B - int(color_data.loc[i, "B"]))
        if distance <= min_distance:
            min_distance = distance
            closest_color_name = color_data.loc[i, "color_name"]
    return closest_color_name

# Function to get x, y coordinates of a double click event
def handle_double_click(event, x, y, flags, param):
    if event == cv2.EVENT_LBUTTONDBLCLK:
        global blue, green, red, x_pos, y_pos, is_clicked
        is_clicked = True
        x_pos = x
        y_pos = y
        blue, green, red = image[y, x]
        blue = int(blue)
        green = int(green)
        red = int(red)

# Create a fixed-size window
cv2.namedWindow('image', cv2.WINDOW_NORMAL)
cv2.resizeWindow('image', window_width, window_height)
cv2.setMouseCallback('image', handle_double_click)

while True:
    cv2.imshow("image", image)
    if is_clicked:
        # Draw a rectangle with the selected color
        cv2.rectangle(image, (20, 20), (750, 60), (blue, green, red), -1)

        # Create text string to display color name and RGB values
        color_name = get_color_name(red, green, blue)
        text = f"{color_name} R={red} G={green} B={blue}"

        # Add the text to the image
        cv2.putText(image, text, (50, 50), cv2.FONT_HERSHEY_SIMPLEX, 0.8, (255, 255, 255), 2, cv2.LINE_AA)

        # For very light colors, display the text in black
        if red + green + blue >= 600:
            cv2.putText(image, text, (50, 50), cv2.FONT_HERSHEY_SIMPLEX, 0.8, (0, 0, 0), 2, cv2.LINE_AA)

        is_clicked = False

    # Break the loop when the user hits the 'esc' key or clicks the cross button
    key = cv2.waitKey(20)
    if key == 27 or cv2.getWindowProperty('image', cv2.WND_PROP_VISIBLE) < 1:
        break

cv2.destroyAllWindows()
