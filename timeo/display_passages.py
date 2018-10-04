# -*- coding: utf-8 -*-


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


def cli_display(description, messages, passages):
    """Text output"""

    print('\n-----DESCRIPTION-----')
    print('Arrêt : {0} [CODE] : {1}'.format(description['arret'], description['code']))
    print('Ligne {0}'.format(description['ligne_nom']))

    # TODO: Ajouter "Passage dans XX minutes" si la durée est inférieure à 30 minutes
    # TODO: Ajouter "Passage imminent" si la durée est inférieure à 2 minutes
    print('\n-----PASSAGES-----')
    print('Prochain passage à {0} pour {1}'.format(passages[0]['duree'], passages[0]['destination']))
    print('Passage suivant à {0} pour {1}'.format(passages[1]['duree'], passages[1]['destination']))

    len(messages)
    list(messages)
    print(messages)
    if len(messages) > 0:
        print('\n-----MESSAGES-----')
        if len(messages) > 1:
            for message in messages:
                print("/!\\", message['titre'], ':')
                print("\t", message['texte'])
        else:
                print("/!\\", messages['titre'], ':')
                print("\t", messages['texte'])
