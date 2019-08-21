# -*- coding: utf-8 -*-
import pandas as pd
import urllib
import xmltodict

from parameters import get_url_times


def get_lines():
    df_lines = pd.read_csv('data/codes_lignes.csv', index_col=False)
    return df_lines


def get_stops():
    df_stops = pd.read_csv('data/codes_arrets.csv', index_col=False)
    return df_stops


def get_alerts(only_bloquant=True):

    xml_times = urllib.request.urlopen(get_url_times('269060357|269059845'))
    data_xml = xml_times.read()
    xml_times.close()
    data_dict = xmltodict.parse(data_xml)

    try:
        list_alerts = data_dict['xmldata']['reseau']

        if list_alerts['titre'] is None and list_alerts['texte'] is None:
            return None

        if list_alerts['bloquant'] == 'true' and only_bloquant:
            return (list_alerts['titre'], list_alerts['texte'])
        elif list_alerts['bloquant'] == 'true' and not only_bloquant:
            return None
        elif list_alerts['bloquant'] == 'false' and only_bloquant:
            return None
        else:
            return (list_alerts['titre'], list_alerts['texte'])

    except KeyError:
        return None


def get_times(ref_arret):
    """We suppose the ref is valid."""
    # Decode XML
    print(get_url_times(ref_arret))
    xml_times = urllib.request.urlopen(get_url_times(ref_arret))
    data_xml = xml_times.read()
    xml_times.close()

    data_dict = xmltodict.parse(data_xml)
    # print(data_dict)
    list_times = data_dict['xmldata']['horaires']['horaire']

    # Get data
    description = list_times['description']
    try:
        messages = list_times['messages']['message']

    except KeyError:
        messages = []

    try:
        passages = list_times['passages']['passage']

    except KeyError:
        passages = []

    return description, messages, passages
