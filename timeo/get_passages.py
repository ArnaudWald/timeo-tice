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


def find_stops_from_code(df_stops, code_input, code_ligne=None):
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
        nom_arret = stops.nom_arret.iloc[0]
        print("Faites votre choix parmi les lignes suivantes pour l'arrêt {0} ({1})".format(nom_arret, code_input))
        i_min, i_max = pretty_print_ligne(stops)
        code_ligne = stops.code_ligne.iloc[bounded_int_input(i_min, i_max)]

        return find_stops_from_code(df_stops, code_input, code_ligne)

    else:
        # Only one possibility : return refs
        return stops.refs.iloc[0]


def find_stops_from_name(df_stops, name_input):

    stop_names = df_stops[df_stops['nom_arret'].apply(lambda x: x.lower()).str.contains(name_input.lower())]

    if stop_names.shape[0] == 0:
        # L'entrée ne correspond à aucun arrêt connu
        # Exemple : 'xxvzf'
        print('Aucun code ne correspond')
        return False

    elif len(set(stop_names.nom_arret)) != 1:
        # Entrée valide, mais plusieurs arrêts possibles
        # Exemple : 'ga'
        print('Veuillez affiner votre recherche parmi les arrêts suivants')
        pretty_print_arrets(stop_names)
        return False

    elif len(set(stop_names.nom_ligne)) != 1:
        # Un seul arret, mais plusieurs lignes possibles
        # Exemple : 'garenne'
        nom_arret = stop_names.nom_arret.iloc[0]
        codes_arret = [str(code) for code in list(set(stop_names.code_arret))]
        print("Faites votre choix parmi les lignes suivantes pour l'arrêt {0} ({1})".format(nom_arret, ', '.join(codes_arret)))
        pretty_print_ligne(stop_names)
        return True

    elif len(set(stop_names.sens)):
        # Une seule ligne, mais plusieurs directions possibles
        # Exemple : 'donjon'
        nom_arret = stop_names.nom_arret.iloc[0]
        codes_arret = [str(code) for code in list(set(stop_names.code_arret))]
        nom_ligne = stop_names.nom_ligne.iloc[0]
        print("Faites votre choix parmi les directions suivantes pour l'arrêt {0} de la ligne {2} ({1})".format(nom_arret, ', '.join(codes_arret), nom_ligne))
        pretty_print_ligne(stop_names)
        return True

    else:
        # Cas qui ne devrait pas arriver
        return True


def get_times(ref_arret):
    """We suppose the ref is valid"""

    xml_times = urllib.request.urlopen(get_url_times(ref_arret))
    data_xml = xml_times.read()
    xml_times.close()

    data_dict = xmltodict.parse(data_xml)
    list_times = data_dict['xmldata']['horaires']['horaire']
    list_times
    description = list_times['description']
    try:
        messages = list_times['messages']['message']
    except KeyError:
        messages = []
    passages = list_times['passages']['passage']

    return description, messages, passages


if __name__ == '__main__':
    df_stops = get_stops()
    ref_arret = find_stops_from_code(df_stops, 0)

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
