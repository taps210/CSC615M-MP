import PySimpleGUI as sg

def main():
    layout = [
        [sg.Text("Machine Definition:")],
        [sg.Multiline(size=(60, 20), key='-DEFINITION-')],
        [sg.Text("Input String:")],
        [sg.Multiline(size=(60, 5), key='-INPUT-')],
        [sg.Button("Execute")],
        [sg.Text("Execution Steps:")],
        [sg.Multiline(size=(60, 10), key='-OUTPUT-')]
    ]

    window = sg.Window("Abstract Machine Interpreter", layout)

    while True:
        event, values = window.read()
        if event == "Execute":
            # Execute machine logic here
            pass
        elif event == sg.WINDOW_CLOSED:
            break

    window.close()

if __name__ == "__main__":
    main()
