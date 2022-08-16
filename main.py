import PySimpleGUI as sg
import autocompletion as ac
from geneanet import Geneanet
import layouts



def make_window(title, layout, theme=None):
    if theme:
        sg.theme(theme)

    return sg.Window(title, layout)

def main():

    # Create the window and show it without the plot
    window = make_window('Généalogie', layouts.window, 'DarkAmber')
    geneanet = Geneanet()
    while True:
        event, values = window.read()
        if event == 'Exit' or event == sg.WIN_CLOSED:
            break
        print(event)
        if event == 'À propos...':
            window.disappear()
            sg.popup('À propos de ce programme', 'Version alpha',
                     'PySimpleGUI Version', sg.version, 'Créé par Séverin Robert',  grab_anywhere=True)
            window.reappear()
        elif event == 'Thèmes':
            event, values = sg.Window('Choose Theme', [[sg.Combo(sg.theme_list(), readonly=True, k='-THEME-'), sg.OK(), sg.Cancel()]]).read(close=True)
            if event == 'OK':
                window.close()
                window = make_window('Généalogie', layouts.window, values['-THEME-'])
        elif event == '-SEARCHMARRIAGELOCATION-':
            location_list = geneanet.location_autocompletion(values['-SEARCHMARRIAGELOCATION-'])
            window['-COMBOMARRIAGELOCATION-'].update(value=location_list[1], values=location_list[1:])
        

    window.close()

if __name__ == '__main__':
    main()