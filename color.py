import cv2
import numpy as np
import pandas as pd
import argparse

# Creating argument parser to take image path from command line
ap = argparse.ArgumentParser()
ap.add_argument('-i', '--image', required=True, help="C://Users//sirij//Downloads//testimg.png")
args = vars(ap.parse_args())
img_path = args['image']

# Reading the image with OpenCV
img = cv2.imread(img_path)

# Declaring global variables
clicked = False
r = g = b = xpos = ypos = 0

# Reading CSV file with pandas and naming columns
index = ["color", "color_name", "hex", "R", "G", "B"]
csv = pd.read_csv('colors.csv', names=index, header=None)

# Function to calculate minimum distance from all colors and get the closest match
def getColorName(R, G, B):
    minimum = float('inf')
    cname = ""
    for i in range(len(csv)):
        d = abs(R - int(csv.loc[i, "R"])) + abs(G - int(csv.loc[i, "G"])) + abs(B - int(csv.loc[i, "B"]))
        if d < minimum:
            minimum = d
            cname = csv.loc[i, "color_name"]
    return cname

# Function to get x, y coordinates of mouse double click
def draw_function(event, x, y, flags, param):
    global b, g, r, xpos, ypos, clicked
    if event == cv2.EVENT_LBUTTONDBLCLK:
        clicked = True
        xpos, ypos = x, y
        b, g, r = img[y, x]
        b, g, r = int(b), int(g), int(r)

# Creating window and setting mouse callback
cv2.namedWindow('image')
cv2.setMouseCallback('image', draw_function)

while True:
    cv2.imshow("image", img)
    
    if clicked:
        cv2.rectangle(img, (20, 20), (750, 60), (b, g, r), -1)
        text = getColorName(r, g, b) + f' R={r} G={g} B={b}'
        
        # Display text in white or black depending on brightness
        text_color = (255, 255, 255) if (r + g + b < 600) else (0, 0, 0)
        cv2.putText(img, text, (50, 50), cv2.FONT_HERSHEY_SIMPLEX, 0.8, text_color, 2, cv2.LINE_AA)
        
        clicked = False

    # Break the loop when user hits 'esc' key
    if cv2.waitKey(20) & 0xFF == 27:
        break

cv2.destroyAllWindows()
