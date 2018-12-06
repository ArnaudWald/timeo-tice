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


def get_alerts(bloquant=True):

    xml_times = urllib.request.urlopen(get_url_times('269060357|269059845'))
    data_xml = xml_times.read()
    xml_times.close()
    data_dict = xmltodict.parse(data_xml)

    try:
        list_alerts = data_dict['xmldata']['reseau']
        bloquant = str(bloquant).lower()

        if list_alerts['bloquant'] == bloquant:
            return (list_alerts['titre'], list_alerts['texte'])
        else:
            return None

    except KeyError:
        return None


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
        messages = []

    try:
        passages = list_times['passages']['passage']

    except KeyError:
        passages = []

    return description, messages, passages
