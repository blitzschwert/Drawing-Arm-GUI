from pickle import TRUE
import sys
import PySimpleGUI as sg
from PIL import ImageGrab

sg.theme('DarkAmber')

layout = [  [sg.Text('Draw a picture with the left mouse button')],
            [sg.Graph(canvas_size = (1280, 720), graph_bottom_left = (0, 0), graph_top_right = (1280, 720), 
            enable_events = TRUE, background_color = 'white', key = 'CANVAS', drag_submits = TRUE)],
            [sg.Button('Done')]]

window = sg.Window('Test drawing', layout)
canvas = window['CANVAS']


while TRUE:
    event, values = window.read()
    if event == sg.WIN_CLOSED or event == 'Done':
        break
    if event == 'CANVAS':
        x, y = values['CANVAS']
        canvas.draw_point((x, y,), size = 6)
        print(y)

widget = canvas.Widget
box = (widget.winfo_rootx(), widget.winfo_rooty(), widget.winfo_rootx() + widget.winfo_width(), widget.winfo_rooty() + widget.winfo_height())
grab = ImageGrab.grab(bbox = box)
grab.save(picture)