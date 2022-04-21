import PySimpleGUI as sg

layout = [[sg.Text('This is a placeholder program'), sg.Button('Ok')]]

window = sg.Window('Temp', layout)

while True:
    event, values = window.read()
    if event == sg.WIN_CLOSED or event == 'Ok':
        break

window.close()