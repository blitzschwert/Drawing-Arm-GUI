# Author:   Craig Brod
# Created:  4.17.2022

import PySimpleGUI as sg
import os
import subprocess as sp
import serial as s
import time

# Set the color theme for the GUI
sg.theme('DarkAmber')

# Start up serial communication
arm = s.Serial()
arm.baudrate = 9600
arm.port = 'COM4'
arm.timeout = 2

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
    
    # Open connection to arm
        arm.open()
        time.sleep(2)

    # Send codes to arm and wait between each
        for code in codes:
            arm.write(code.encode())
            print(code)
            msg = arm.readline()
            print(msg.decode())
        if True:
            break

    arm.close()
    presets_window.close()

# Create layout for main GUI
layout = [  [sg.Text('Pick an option')],
            [sg.Text('Presets')],
            [sg.Button('Line'), sg.Button('Square'), sg.Button('Circle'), sg.Button('Heart'), sg.Button('Star')],
            [sg.Text('Custom')],
            [sg.Button('Drawing'), sg.Button('Import Image'), sg.Button('Take Picture')]  ]

# Open GUI window
main_window = sg.Window('Drawing Arm Control', layout)

# Enter window loop
while True:
    event, values = main_window.read()
    if event == sg.WIN_CLOSED:
        break
    elif event == 'Line' or event == 'Square' or event == 'Circle' or event == 'Heart' or event == 'Star':
        presets(event)
    elif event == 'Drawing':
        sp.call('python ./cvmain.py -d')
    elif event == 'Import Image':
        sp.call('python ./cvmain.py -i')
    elif event == 'Take Picture':
        sp.call('python ./cvmain.py -p')

# Close window
main_window.close()