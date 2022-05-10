import sys
import PySimpleGUI as sg

sg.theme('DarkAmber')

def setMode(option):
    if option == "-d" or option == "draw":
        print("drawing mode")
    elif option == "-i" or option == "import":
        filename = sg.popup_get_file('Picture to copy')
        print(filename)
        print("import mode")
    elif option == "-p" or option == "picture":
        print("picture mode")

to_display = sys.argv[1]
print(to_display)
setMode(to_display)