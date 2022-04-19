import PySimpleGUI as sg

sg.theme('DarkAmber')

layout = [  [sg.Text('Test')],
            [sg.Button('Yes'), sg.Button('No')]  ]

main_window = sg.Window('Window Title', layout)

while True:
    event, values = main_window.read()
    if event == sg.WIN_CLOSED:
        break

main_window.close()