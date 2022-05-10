import numpy as np
import cv2 as cv
import PySimpleGUI as sg
import sys

sg.theme('DarkAmber')

option = sys.argv[1]

if option == '-d' or option == 'draw':
    layout = [  [sg.Text('Draw an Image')],
                [sg.Text('This is where the drawing box will go')],
                [sg.Button('Done')] ]
    print('drawing mode')

elif option == '-i' or option == 'import':
    picture = sg.popup_get_file('What picture do you want to copy?')
    print('import mode')

elif option == '-p' or option == 'picture':
    picture = 'temp_img.png'
    layout = [  [sg.Text('Please make sure webcam is unobstrucked')],
                [sg.Image(filename = '', key = 'image')],
                [sg.Button('Take picture'), sg.Button('Done')]  ]

    window = sg.Window('Webcam Feed', layout)

    cam = cv.VideoCapture(0)
    cam.set(cv.CAP_PROP_FRAME_WIDTH, 1280)
    cam.set(cv.CAP_PROP_FRAME_HEIGHT, 720)

    while True:
        event, values = window.read(timeout = 20)
        if event == 'Done' or event == sg.WIN_CLOSED:
            break
        trash, frame = cam.read()
        imgbytes = cv.imencode('.png', frame)[1].tobytes()
        window['image'].update(data = imgbytes)
        if event == 'Take picture':
            cv.imwrite(picture, frame)
    window.Close()
    print('picture mode')

img = cv.imread(picture, cv.IMREAD_GRAYSCALE)
ret, thresh = cv.threshold(img, 127, 255, cv.THRESH_BINARY)
contours, hierarchy = cv.findContours(thresh, cv.RETR_TREE, cv.CHAIN_APPROX_SIMPLE)

f = open('data_to_send.txt', 'w')

accuracy = 0.009
b = 0
for cnt in contours:
    f.write('G0 X0 Y0\n')
    b = b + 1
    approx = cv.approxPolyDP(cnt, accuracy * cv.arcLength(cnt, True), True)

    n = approx.ravel()
    i = 0
    for j in n:
        if (i % 2 == 0):
            x = repr(n[i])
            y = repr(n[i + 1])
            f.write('G1 X' + x + ' Y' + y + '\n')
        i = i + 1

imgx, imgy = img.shape
img = np.zeros((imgx,imgy,3), np.uint8)
cv.drawContours(img, contours, -1, (0,255,0), 3)
cv.imwrite('test.png', img)