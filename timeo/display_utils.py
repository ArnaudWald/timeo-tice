# -*- coding: utf-8 -*-
from datetime import datetime
from get_passages import get_alerts


def bounded_int_input(i_min, i_max):

    input_ok = False
    int_input = -1

    while not input_ok:

        try:
            int_input = int(input("Entrez le nombre correspondant à votre choix : "))

            if int_input >= i_min and int_input <= i_max:
                input_ok = True

            else:
                print('Le nombre doit être compris entre {0} et {1}'.format(i_min, i_max))

        except ValueError:
            print('Entrée invalide, essayez à nouveau.')

    return int_input


def pretty_print_ligne(df):
    i = 0

    for index, row in df.iterrows():
        print("    {0}. Ligne {1} > {2}".format(i, row['nom_ligne'], row['vers']))
        i += 1

    return 0, i-1


def pretty_print_arrets(df):
    names = sorted(list(set(df.nom_arret)))
    i = 0

    for index, row in enumerate(names):
        print("    {0}. {1}".format(i, names[i]))
        i += 1

    return 0, i-1


def time_difference(passage_):
    fmt = '%H:%M'

    now_ = datetime.now().strftime(fmt)
    now_ = datetime.strptime(now_, fmt)

    passage_ = datetime.strptime(passage_, fmt)

    diff = int((passage_ - now_).seconds / 60)

    return diff


def show_alerts(alerts, bloquant=True):

    if alerts is not None:
        if bloquant:
            print("❌  Impossible d'utiliser le service actuellement ❌")
            print("Motif :", alerts[0])
            print(alerts[1])
            exit()

        else:
            print("⚠️  En ce moment sur le réseau ⚠️")
            print(alerts[0])
            print(alerts[1])


def cli_display(description, messages, passages):
    """Text output"""

    other_alerts = get_alerts(bloquant=False)
    show_alerts(other_alerts, bloquant=False)

    print('\n-----DESCRIPTION-----')
    print('  ▶️   Arrêt : {0}'.format(description['arret']))
    print('  ▶️   Code : {0}'.format(description['code']))
    print('  ▶️   Ligne {0}'.format(description['ligne_nom']))

    print('\n-----PASSAGES-----')

    if len(passages) == 0:
        print("Aucun horaire n'est actuellement disponible pour cet arrêt.")

    for i, passage in enumerate(passages):
        horaire = passages[i]['duree']
        diff = time_difference(horaire)

        if diff == 0:
            print("Passage en cours", end='')

        elif diff <= 2:
            print("Passage imminent", end='')

        else:
            if i == 0:
                print("Prochain passage", end='')

            else:
                print("Passage suivant", end='')

            if diff < 60:
                print(" dans {0} minutes".format(diff), end='')

            else:
                print(" à {0}".format(horaire), end='')

        print(" pour {0}".format(passages[1]['destination']))

    if len(messages) > 0:
        print('\n-----MESSAGES-----')

        if isinstance(messages, list):
            # Multiple messages
            for message in messages:

                if message['bloquant'] == 'true':
                    print("❌", message['titre'], ':')

                else:
                    print("⚠️", message['titre'], ':')

                print("    ", message['texte'])

        else:
            # Only one message
            if messages['bloquant'] == 'true':
                print("❌", messages['titre'], ':')

            else:
                print("⚠️", messages['titre'], ':')

            print("    ", messages['texte'])
