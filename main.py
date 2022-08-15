import PySimpleGUI as sg
import autocompletion as ac
from layouts import layout


def main():

    sg.theme('LightGreen')

    # Create the window and show it without the plot
    window = sg.Window('Généalogie', layout, location=(800, 400))
    while True:
        event, values = window.read()
        if event == 'Exit' or event == sg.WIN_CLOSED:
            break
        print(event)
        if event == '-BACK-':
            pass
        elif event == '-SEARCHMARRIAGELOCATION-':
            location_list = ac.search(values['-SEARCHMARRIAGELOCATION-'])
            window['-COMBOMARRIAGELOCATION-'].update(value=location_list[1], values=location_list[1:])

    window.close()

if __name__ == '__main__':
    main()