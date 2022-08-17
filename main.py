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

def update_combo(combo:sg.Combo, items:list):
    '''Update the given combo with the given items'''
    if items != []:
        combo.update(value=items[0], values=items)
    else:
        combo.update(value=[], values=[])

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
        
        # When the user write a place, search for autocompletion
        elif event in ('-BIRTHPLACE-', '-DEATHPLACE-', '-MARRIAGEPLACE-'):
            place_list = geneanet.place_autocompletion(values[event])
            update_combo(window[f'-COMBO{event[1:-1]}-'], place_list)
        # When an option in a COMBO is selected, update the corresponding field
        elif event in ('-COMBOPARENT-', '-COMBOBORNPLACE-', '-COMBODEATHPLACE-', '-COMBOMARRIAGEPLACE-', '-COMBOPARTNER-'):
            window[f'-{event[6:]}'].update(value=values[event])
        # When the user write a person, search for autocompletion in the family tree
        elif event in ('-PARTNER-', '-PARENT-'):
            partner_list = geneanet.person_autocompletion(values[event])
            update_combo(window[f'-COMBO{event[1:-1]}-'], partner_list)
        # When the user click on the add button, add the person to the family tree
        elif event == '-ADD-':
            geneanet.add_person(values)

    window.close()

if __name__ == '__main__':
    main()
