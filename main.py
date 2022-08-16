'''This module starts and runs the program'''

import PySimpleGUI as sg
from geneanet import Geneanet
import layouts


def make_window(title:str, layout:list, theme:str=None):
    '''Make a window with the given title, layout and theme

        Args:
            title (str): The title of the window
            layout (list): The layout of the window
            theme (str): The theme of the window

        Returns:
            sg.Window: The window
    '''
    if theme:
        sg.theme(theme)

    return sg.Window(title, layout)

def main():
    '''Main function of the program'''

    # Create the window and show it without the plot
    window = make_window('Généalogie', layouts.window, 'DarkAmber')
    geneanet = Geneanet()

    while True:
        event, values = window.read()
        if event in ('Exit', sg.WIN_CLOSED, 'Quitter le programme'):
            break
        print(event, values)
        if event == 'À propos...':
            window.disappear()
            sg.popup('À propos de ce programme', 'Version alpha', 'PySimpleGUI Version', 
                    sg.version, 'Créé par Séverin Robert',  grab_anywhere=True)
            window.reappear()
        elif event == 'Thèmes':
            event, values = sg.Window('Choisir un thème', layouts.theme).read(close=True)
            if event == 'OK':
                window.close()
                window = make_window('Généalogie', layouts.window, values['-THEME-'])
        elif event == 'Sécurité':
            event, values = sg.Window('Choisir un mot de passe', layouts.security).read(close=True)
            if event == 'OK':
                pass

        elif event in ('-BORNPLACE-', '-DEATHPLACE-', '-MARRIAGEPLACE-'):
            place_list = geneanet.place_autocompletion(values[event])
            if place_list != []:
                window[f'-COMBO{event[1:-1]}-'].update(value=place_list[0], values=place_list[0:])
            else:
                window[f'-COMBO{event[1:-1]}-'].update(value=[], values=[])
        elif event in ('-COMBOPARENT-', '-COMBOBORNPLACE-', '-COMBODEATHPLACE-', '-COMBOMARRIAGEPLACE-', '-COMBOPARTNER-'):
            window[f'-{event[6:]}'].update(value=values[event])
        elif event in ('-PARTNER-', '-PARENT-'):
            partner_list = geneanet.person_autocompletion(values[event])
            if partner_list != []:
                window[f'-COMBO{event[1:-1]}-'].update(value=partner_list[0], values=partner_list[0:])
            else:
                window[f'-COMBO{event[1:-1]}-'].update(value=[], values=[])
        elif event == '-ADD-':
            geneanet.add_person(values)

    window.close()

if __name__ == '__main__':
    main()
