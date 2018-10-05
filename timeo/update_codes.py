# -*- coding: utf-8 -*-
import os
import pandas as pd
import urllib
import xmltodict

from parameters import get_url_all_lines, get_url_stop_codes


def update_all_lines(filename):
    """
        Reload the csv with all the lines, codes etc.
    """
    xml_lines = urllib.request.urlopen(get_url_all_lines())
    data_xml = xml_lines.read()
    xml_lines.close()

    data_dict = xmltodict.parse(data_xml)
    list_lines = data_dict['xmldata']['alss']['als']

    columns = ['code_ligne', 'nom_ligne', 'sens', 'vers', 'couleur']
    data = dict([(key, []) for key in columns])

    for line in list_lines:
        line = line['ligne']
        data['code_ligne'].append(line['code'])
        data['nom_ligne'].append(line['nom'])
        data['sens'].append(line['sens'])
        data['vers'].append(line['vers'])
        data['couleur'].append(line['couleur'])

    data = pd.DataFrame.from_dict(data).astype('str')

    data.to_csv(filename, index=False)

    return data


def update_stop_codes(code_ligne, sens, filename):
    """
    Reload the csv with all the stop codes, names etc.
    """

    xml_stops = urllib.request.urlopen(get_url_stop_codes(code_ligne, sens))
    data_xml = xml_stops.read()
    xml_stops.close()

    data_dict = xmltodict.parse(data_xml)
    list_stops = data_dict['xmldata']['alss']['als']

    columns = ['code_ligne', 'nom_ligne', 'sens', 'vers', 'couleur', 'code_arret', 'nom_arret', 'refs']
    data = dict([(key, []) for key in columns])

    for stop in list_stops:
        line = stop['ligne']
        data['refs'].append(stop['refs'])
        stop = stop['arret']
        data['code_ligne'].append(line['code'])
        data['nom_ligne'].append(line['nom'])
        data['sens'].append(line['sens'])
        data['vers'].append(line['vers'])
        data['couleur'].append(line['couleur'])
        data['code_arret'].append(stop['code'])
        data['nom_arret'].append(stop['nom'])

    data = pd.DataFrame.from_dict(data).astype('str')

    data = data[data['code_arret'] != '0']

    if not os.path.isfile(filename):
        data.to_csv(filename, index=False)
    else:
        data.to_csv(filename, mode='a', header=False, index=False)

    return data


if __name__ == '__main__':
    filename = 'timeo/data/codes_lignes.csv'
    updated_lines = update_all_lines(filename)

    filename = 'timeo/data/codes_arrets.csv'
    if os.path.isfile(filename):
        os.remove(filename)

    for index, row in updated_lines.loc[:, ['code_ligne', 'sens']].iterrows():
        update_stop_codes(row.code_ligne, row.sens, filename)
