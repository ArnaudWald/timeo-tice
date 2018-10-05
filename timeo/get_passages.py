# -*- coding: utf-8 -*-
import pandas as pd
import urllib
import xmltodict

from timeo.parameters import get_url_times
from timeo.display_passages import pretty_print_ligne, pretty_print_arrets, \
    bounded_int_input, cli_display


def get_lines():
    df_lines = pd.read_csv('timeo/data/codes_lignes.csv', index_col=False)
    return df_lines


def get_stops():
    df_stops = pd.read_csv('timeo/data/codes_arrets.csv', index_col=False)
    return df_stops


def find_refs(df_stops, refs):
    return df_stops[df_stops['refs'] == refs]


def find_stops_from_code(df_stops, code_input, code_ligne=None,
                         first_try=True):
    """ We assume code_input and code_ligne are integer """
    stops = df_stops[df_stops['code_arret'] == code_input]

    if code_ligne is not None:
        stops = stops[stops['code_ligne'] == code_ligne]

    if stops.shape[0] == 0:
        # Code invalide
        # Exemple : '0', '231009', 'toto'....
        print('Aucun arrêt trouvé')
        return False

    elif stops.shape[0] > 1:
        # Code valide mais plusieurs lignes possibles :
        # on demande des précisions à l'utilisateur
        # Exemple : 1139
        if first_try:
            nom_arret = stops.nom_arret.iloc[0]
            print("Faites votre choix parmi les lignes suivantes pour l'arrêt {0} ({1})".format(nom_arret, code_input))
            i_min, i_max = pretty_print_ligne(stops)
            code_ligne = stops.code_ligne.iloc[bounded_int_input(i_min, i_max)]
            return find_stops_from_code(df_stops, code_input, code_ligne, first_try=False)
        else:
            print('Erreur')
            return False
    else:
        # Only one possibility : return refs
        return stops.refs.iloc[0]


def find_stops_from_name(df_stops, name_input, code_ligne=None, sens=None,
                         first_try_arret=True,
                         first_try_ligne=True,
                         first_try_sens=True):

    stops = df_stops[df_stops['nom_arret'].apply(lambda x: x.lower()).str.contains(name_input.lower())]

    if code_ligne is not None:
        stops = stops[stops['code_ligne'] == code_ligne]
    if sens is not None:
        stops = stops[stops['sens'] == sens]

    if stops.shape[0] == 0:
        # L'entrée ne correspond à aucun arrêt connu
        # Exemple : 'xxvzf'
        print('Aucun code ne correspond')
        return False

    elif len(set(stops.nom_arret)) != 1:
        # Entrée valide, mais plusieurs arrêts possibles
        # Exemple : 'ga'
        if first_try_arret:
            print('Veuillez affiner votre recherche parmi les arrêts suivants')
            i_min, i_max = pretty_print_arrets(stops)
            name_input = stops.nom_arret.iloc[bounded_int_input(i_min, i_max)]
            return find_stops_from_name(df_stops, name_input, code_ligne, sens,
                                        first_try_arret=False,
                                        first_try_ligne=first_try_ligne,
                                        first_try_sens=first_try_sens)
        else:
            print('Erreur')
            return False

    elif len(set(stops.nom_ligne)) != 1:
        # Un seul arret, mais plusieurs lignes possibles
        # Exemple : 'garenne'
        if first_try_ligne:
            nom_arret = stops.nom_arret.iloc[0]
            codes_arret = [str(code) for code in list(set(stops.code_arret))]
            print("Faites votre choix parmi les lignes suivantes pour l'arrêt {0} ({1})".format(nom_arret, ', '.join(codes_arret)))
            i_min, i_max = pretty_print_ligne(stops)
            i_input = bounded_int_input(i_min, i_max)
            code_ligne = stops.code_ligne.iloc[i_input]
            sens = stops.sens.iloc[i_input]

            return find_stops_from_name(df_stops, nom_arret, code_ligne, sens,
                                        first_try_arret=first_try_arret,
                                        first_try_ligne=False,
                                        first_try_sens=first_try_sens)
        else:
            print('Erreur')
            return False

    elif len(set(stops.sens)) != 1:
        # Une seule ligne, mais plusieurs directions possibles
        # Exemple : 'donjon'
        if first_try_sens:
            nom_arret = stops.nom_arret.iloc[0]
            codes_arret = [str(code) for code in list(set(stops.code_arret))]
            nom_ligne = stops.nom_ligne.iloc[0]
            print("Faites votre choix parmi les directions suivantes pour l'arrêt {0} de la ligne {2} ({1})".format(nom_arret, ', '.join(codes_arret), nom_ligne))
            i_min, i_max = pretty_print_ligne(stops)
            sens = stops.sens.iloc[bounded_int_input(i_min, i_max)]

            return find_stops_from_name(df_stops, nom_arret, nom_ligne, sens,
                                        first_try_arret=first_try_arret,
                                        first_try_ligne=first_try_ligne,
                                        first_try_sens=False)
        else:
            print('Erreur')
            return False
    else:
        # On renvoie la bonne data
        return stops.refs.iloc[0]


def find_stops_from_line(df_stops):
    list_lignes = df_stops.drop_duplicates(['code_ligne', 'sens'])

    print('Sélectionnez une ligne')
    i_min, i_max = pretty_print_ligne(list_lignes)
    i_input = bounded_int_input(i_min, i_max)
    code_ligne = list_lignes.code_ligne.iloc[i_input]
    sens_ligne = list_lignes.sens.iloc[i_input]

    list_stops = df_stops[df_stops['code_ligne'] == code_ligne]
    list_stops = list_stops[list_stops['sens'] == sens_ligne]

    print('Faites votre choix parmi les arrêt des la ligne {0} > {1}'.format(list_stops.nom_ligne.iloc[0], list_stops.vers.iloc[0]))
    i_min, i_max = pretty_print_arrets(list_stops)
    i_input = bounded_int_input(i_min, i_max)

    return list_stops.refs.iloc[i_input]


def get_times(ref_arret):
    """We suppose the ref is valid"""

    # Decode XML
    xml_times = urllib.request.urlopen(get_url_times(ref_arret))
    data_xml = xml_times.read()
    xml_times.close()

    data_dict = xmltodict.parse(data_xml)
    list_times = data_dict['xmldata']['horaires']['horaire']

    # Get data
    description = list_times['description']
    try:
        messages = list_times['messages']['message']
    except KeyError:
        messages
    try:
        passages = list_times['passages']['passage']
    except KeyError:
        passages = []

    return description, messages, passages


if __name__ == '__main__':
    df_stops = get_stops()

    # Cas numéro 1 : on saisit le code d'un arrêt
    stop_code_input = ''
    num_tries = 0
    ref_arret = False

    while num_tries < 10 and not ref_arret:
        num_tries += 1
        try:
            stop_code_input = int(input('Entrez un code arrêt : '))
            ref_arret = find_stops_from_code(df_stops, stop_code_input)
        except ValueError:
            print("Veuillez saisir un code valide")

    # ref_arret = find_stops_from_code(df_stops, stop_code_input)
    if ref_arret is not False:
        description, messages, passages = get_times(ref_arret)
        cli_display(description, messages, passages)
    else:
        print('Echec')

    # Cas numéro 2 : on saisit un nom d'arrêt
    stop_name_input = ''
    num_tries = 0
    ref_arret = False

    while num_tries < 10 and not ref_arret:
        num_tries += 1

        stop_name_input = input("Entrez le nom de l'arrêt : ")
        ref_arret = find_stops_from_name(df_stops, stop_name_input)

    if ref_arret is not False:
        description, messages, passages = get_times(ref_arret)
        cli_display(description, messages, passages)
    else:
        print('Echec')

    # Cas numéro 3 : on sélectionne directement la ligne puis l'arrêt
    ref_arret = find_stops_from_line(df_stops)

    if ref_arret is not False:
        description, messages, passages = get_times(ref_arret)
        cli_display(description, messages, passages)
    else:
        print('Echec')
