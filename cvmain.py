# Author:       Craig Brod
# Created:      5.4.2022
# Description:  This project is meant to act as a subprocess for our main GUI and handles the processing
#               of images into contour lines and then into GCODE. This subprocess requires an option in
#               the command line call to access one of three modes: image import, webcam photos, or drawing.
# Sources:      PySimpleGUI Reference (https://pysimplegui.readthedocs.io/en/latest/)
#               OpenCV Tutorials (https://docs.opencv.org/4.x/d6/d00/tutorial_py_root.html)

import numpy as np
import cv2 as cv
import PySimpleGUI as sg
import sys
from PIL import ImageGrab

sg.theme('DarkAmber')

option = sys.argv[1]
picture = 'temp_img.png'

# If this subprocess is called with the '-d' option, activate drawing mode
if option == '-d' or option == 'draw':
    # Create drawing canvas layout
    layout = [  [sg.Text('Draw a picture with the left mouse button')],
                [sg.Graph(  canvas_size = (1280, 720),
                            graph_bottom_left = (0, 0),
                            graph_top_right = (1280, 720), 
                            enable_events = True, 
                            background_color = 'white', 
                            key = 'CANVAS', 
                            drag_submits = True)],
                [sg.Button('Done')]]

    # Open window and create canvas variable for quick access
    window = sg.Window('Test drawing', layout)
    canvas = window['CANVAS']

    # Start window loop
    while True:
        event, values = window.read()
        if event == sg.WIN_CLOSED or event == 'Done':
            break
        # If there is an event on the canvas, draw a point
        elif event == 'CANVAS':
            x, y = values['CANVAS']
            canvas.draw_point((x, y,), size = 6)

    # Pull the data from the canvas object and save it as an image
    widget = canvas.Widget
    box = (widget.winfo_rootx(), widget.winfo_rooty(), widget.winfo_rootx() + widget.winfo_width(), widget.winfo_rooty() + widget.winfo_height())
    grab = ImageGrab.grab(bbox = box)
    grab.save(picture, 'PNG')
    window.close()

# If this subprocess is called with the '-i' option, activate import mode
elif option == '-i' or option == 'import':
    # Get the filename from the user
    picture = sg.popup_get_file('What picture do you want to copy?')

# If this subprocess is called with the '-i' option, activate picture mode
elif option == '-p' or option == 'picture':
    # Create layout for webcam window
    layout = [  [sg.Text('Please make sure webcam is unobstructed')],
                [sg.Image(filename = '', key = 'image')],
                [sg.Button('Take picture'), sg.Button('Done')]  ]

    # Open webcam window
    window = sg.Window('Webcam Feed', layout)

    # Start video capture and set resolution
    cam = cv.VideoCapture(0)
    cam.set(cv.CAP_PROP_FRAME_WIDTH, 1280)
    cam.set(cv.CAP_PROP_FRAME_HEIGHT, 720)

    # Start window loop
    while True:
        event, values = window.read(timeout = 0)
        if event == 'Done' or event == sg.WIN_CLOSED:
            break
        # Read the current frame from the webcam encode it to bytes, and then display it in the window
        trash, frame = cam.read()
        imgbytes = cv.imencode('.png', frame)[1].tobytes()
        window['image'].update(data = imgbytes)

        # Save the picture
        if event == 'Take picture':
            cv.imwrite(picture, frame)
    window.Close()

# Create a grayscale image for processing purposes, then turn it into a black and white image
img = cv.imread(picture, cv.IMREAD_GRAYSCALE)
ret, thresh = cv.threshold(img, 127, 255, cv.THRESH_BINARY)
# Find the contour lines of the image
contours, hierarchy = cv.findContours(thresh, cv.RETR_TREE, cv.CHAIN_APPROX_SIMPLE)

# Open a text file to write the data too
f = open('data_to_send.txt', 'w')

# Set accuracy, counter, and machine origin point
accuracy = 0.009
b = 0
f.write('G0 X0 Y0\n')
for cnt in contours:
    b = b + 1
    # Approximate points on the contour
    approx = cv.approxPolyDP(cnt, accuracy * cv.arcLength(cnt, True), True)

    # Grab x an y coordinates from the approximation
    n = approx.ravel()
    i = 0
    for j in n:
        if (i % 2 == 0):
            # Write points into text file
            x = repr(n[i])
            y = repr(n[i + 1])
            f.write('G1 X' + x + ' Y' + y + '\n')
        i = i + 1

# Create test image for debugging purposes
imgx, imgy = img.shape
img = np.zeros((imgx,imgy,3), np.uint8)
cv.drawContours(img, contours, -1, (0,255,0), 3)
cv.imwrite('test.png', img)
f.close()