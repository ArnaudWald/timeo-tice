# -*- coding: utf-8 -*-
from get_passages import get_stops, get_alerts
from display_utils import show_alerts
from use_cases import use_case_stop_code, use_case_stop_name, \
    use_case_choose_line


def print_intro():
    print('')
    print('Prochains bus')
    print('=============')
    print('Les horaires en temps réel')
    print('')
    print('Consulter les horaires de passage de vos bus :')
    print('    0. Code arrêt')
    print('  OU')
    print("    1. Nom de l'arrêt")
    print('  OU')
    print('    2. Votre ligne')
    print('  OU')
    print('    3. Quitter')
    print('')


def exit_input():
    input("\nPressez n'importe quelle touche pour quitter... ")


if __name__ == '__main__':
    df_stops = get_stops()
    reponse = None

    blocking_alerts = get_alerts(bloquant=True)
    show_alerts(blocking_alerts, bloquant=True)

    other_alerts = get_alerts(bloquant=False)
    show_alerts(other_alerts, bloquant=False)

    print_intro()

    while reponse != 3:
        try:
            reponse = int(input('Faites votre choix parmi les options ci-dessus : '))

            if reponse == 0:
                use_case_stop_code(df_stops)
                exit_input()
                break
            elif reponse == 1:
                use_case_stop_name(df_stops)
                exit_input()
                break
            elif reponse == 2:
                use_case_choose_line(df_stops)
                exit_input()
                break
            elif reponse == 3:
                break
            else:
                print('Entrée non valide')

        except ValueError as e:
            print(e)
            print('Entrée non valide')

    print('À bientôt !')
