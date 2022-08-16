import PySimpleGUI as sg

# Standard layout for the window
input =     lambda text, target_name:       [sg.Text(text), sg.InputText(key=f'-{target_name}-', enable_events=True)]
calendar =  lambda target_name:             sg.CalendarButton('Choisir une date', close_when_date_chosen=True, format='%d/%m/%Y',  target=f'{target_name}', no_titlebar=False)
title =     lambda text:                    [sg.Text(text, size=(60, 1), justification='center')]
date =      lambda input_name, target_name: [sg.Text(f'{input_name}'), sg.InputCombo(['exactement','vers'], ), sg.Text('le'), sg.Input(key=f'-{target_name}-', size=(10,1)), calendar(f'-{target_name}-')]
location =  lambda target_name, locations:  [sg.Text('Lieu'), sg.Input(key=f'-SEARCH{target_name}LOCATION-', size=(10,1), enable_events=True), sg.InputCombo(values=locations, key=f'-COMBO{target_name}LOCATION-', size=(20,1))]
inputCombo = lambda text, values, key_name, width=10: [sg.Text(text), sg.InputCombo(values, key=key_name, size=(width,1))]

# Group of layouts 
# to use it you need to spread it with '*' when you call it (eg. *event('Date de naissance', 'Né(e)', 'BORN', []))
event = lambda title_text, input_name, target_name, locations: [title(title_text), date(input_name, target_name), location(target_name, locations)]

menu_def = [['&Paramètres', ['&Thèmes', '&Sécurité', '&Quitter le programme']],
            ['&Aide', ['&À propos...']]]

# Define the windows layout
add_people = [
    title('Ajouter une personne à l\'arbre'),
    input('Prénom', 'FIRSTNAME'),
    input('Nom', 'LASTNAME'),
    inputCombo('Sexe', ['H', 'F'], '-SEX-', 3),
    *event('Date de naissance', 'Né(e)', 'BORN', []),
    *event('Date du décès', 'Mort(e)', 'DEATH', []),
    *event('Date du mariage', 'Marié(e)', 'MARRIAGE', []),
    [*input('Marié(e) à', 'PARTNER'), sg.Combo([], key='-COMBOPARTNER-', size=(20,1), enable_events=True)],
    [sg.Button('Ajouter un individu', key='-ADD-')]
]

modify_people = [
    title('Modifier une personne existante')
]

window = [[sg.Menu(menu_def)],
    [sg.TabGroup([[sg.Tab('Ajouter une personne', add_people), sg.Tab('Modifier une personne', modify_people)]])]]


