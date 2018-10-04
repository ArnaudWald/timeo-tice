# -*- coding: utf-8 -*-
import pandas as pd
import urllib
import xmltodict

from timeo.parameters import get_url_times


def get_lines():
    df = pd.read_csv('timeo/data/codes_lignes.csv', index_col=False)
    return df


def get_stops():
    df = pd.read_csv('timeo/data/codes_arrets.csv', index_col=False)

    return df


def find_refs(df_stops, code_arret):
    return df_stops[df_stops.code_arret == code_arret]


def get_times(ref_arret):

    xml_times = urllib.request.urlopen(get_url_times(ref_arret))
    data_xml = xml_times.read()
    xml_times.close()

    data_dict = xmltodict.parse(data_xml)
    list_times = data_dict['xmldata']['horaires']['horaire']

    description = list_times['description']
    messages = list_times['messages']['message']
    passages = list_times['passages']['passage']

    return description, messages, passages


if __name__ == '__main__':
    df_stops = get_stops()
    df_stops.dtypes
    code_arret = 1139
    df_stops[df_stops.code_arret == code_arret].refs
    ref_arret = find_refs(df_stops, code_arret)
    ref_arret
    description, messages, passages = get_times(ref_arret)
    messages
    description
    passages
