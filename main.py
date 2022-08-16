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
        if event == 'Exit' or event == sg.WIN_CLOSED or event == 'Quitter le programme':
            break
        print(event, values)
        if event == 'À propos...':
            window.disappear()
            sg.popup('À propos de ce programme', 'Version alpha',
                     'PySimpleGUI Version', sg.version, 'Créé par Séverin Robert',  grab_anywhere=True)
            window.reappear()
        elif event == 'Thèmes':
            event, values = sg.Window('Choisir un thème', [[sg.Combo(sg.theme_list(), readonly=True, k='-THEME-'), sg.OK(), sg.Cancel()]]).read(close=True)
            if event == 'OK':
                window.close()
                window = make_window('Généalogie', layouts.window, values['-THEME-'])
        elif event == 'Sécurité':
            event, values = sg.Window('Choisir un mot de passe', [[sg.Input('', password_char='*', key='-PASSWORD-'), sg.OK(), sg.Cancel()]]).read(close=True)
            if event == 'OK':
                geneanet.set_password(values['-PASSWORD-'])
                window.close()
                window = make_window('Généalogie', layouts.window)

        elif event == '-SEARCHMARRIAGELOCATION-':
            location_list = geneanet.location_autocompletion(values[event])
            if location_list != []:
                window['-COMBOMARRIAGELOCATION-'].update(value=location_list[1], values=location_list[1:])
        elif event == '-PARTNER-':
            partner_list = geneanet.person_autocompletion(values[event])
            if partner_list != []:
                print(partner_list)
                window['-COMBOPARTNER-'].update(value=partner_list[0], values=partner_list[0:])
            else:
                window['-COMBOPARTNER-'].update(value=[], values=[])
        elif event == '-ADD-':
            geneanet.add_person(values)

    window.close()

if __name__ == '__main__':
    main()