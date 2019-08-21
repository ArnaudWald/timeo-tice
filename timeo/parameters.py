# -*- coding: utf-8 -*-
BUS_NETWORK_CODE = '910'


def format_url(xml_key, post_params, bus_network=BUS_NETWORK_CODE):
    return "http://timeo3.keolis.com/relais/{0}.php?xml={1}&{2}".\
        format(bus_network, xml_key, post_params)


def get_url_all_lines():
    """
    URL pour toutes les lignes.

    http://timeo3.keolis.com/relais/<code_réseau>.php?xml=1
    """
    xml_key = 1
    post_params = ''

    return format_url(xml_key, post_params)


def get_url_stop_codes(ligne, sens):
    """
    URL pour les codes d'arrêt.

    http://timeo3.keolis.com/relais/<code_réseau>.php?xml=1&ligne=<id_ligne>&sens=<id_sens>
    """
    xml_key = 1
    post_params = "ligne={0}&sens={1}".format(ligne, sens)

    return format_url(xml_key, post_params)


def get_url_times(ref_arret):
    """
    URL pour les temps de passage.

    http://timeo3.keolis.com/relais/<code_réseau>.php?xml=3&refs=<référence_arret>&ran=1
    """
    xml_key = 3
    post_params = "refs={0}&ran=1".format(ref_arret)

    return format_url(xml_key, post_params)
