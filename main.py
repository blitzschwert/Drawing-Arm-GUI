import PySimpleGUI as sg
import os
import serial as s
import time

# Set the color theme for the GUI
sg.theme('DarkAmber')

# Start up serial communication
arm = s.Serial()
arm.baudrate = 9600
arm.port = 'COM1'

# Create function for when the user selects a preset
def presets(preset):
    presets_layout = [[sg.Text('Please wait...')]]
    presets_window = sg.Window('Sending Codes', presets_layout, modal=True)
    # Create window for user

    while True:
        event, values = presets_window.read(timeout=0)
     # Read lines from the correct preset text file
        with open('./presets/' + preset) as f:
            codes = f.read().splitlines()
    
    # # Open connection to arm
    # while arm.is_open() == False:
    #     arm.open()

    # Send codes to arm and wait between each
        for code in codes:
            # arm.write(code)
            print(code)
            time.sleep(1)
        if True:
            break

    presets_window.close()


layout = [  [sg.Text('Pick an option')],
            [sg.Text('Presets')],
            [sg.Button('Line'), sg.Button('Square'), sg.Button('Circle'), sg.Button('Heart'), sg.Button('Star')],
            [sg.Text('Custom')],
            [sg.Button('Drawing'), sg.Button('Import Image'), sg.Button('Take Picture')]  ]

main_window = sg.Window('Drawing Arm Control', layout)

while True:
    event, values = main_window.read()
    if event == sg.WIN_CLOSED:
        break
    elif event == 'Line' or event == 'Square' or event == 'Circle' or event == 'Heart' or event == 'Star':
        presets(event)

main_window.close()