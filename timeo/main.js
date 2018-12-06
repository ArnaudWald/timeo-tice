// -*- coding: utf-8 -*-
from get_passages var get_stops = require('get_stops');
from use_cases var use_case_stop_code, = require('use_case_stop_code,');


function print_log_intro() {
    console.log('');
    console.log('Prochains bus');
    console.log('=============');
    console.log('Les horaires en temps réel');
    console.log('');
    console.log('Consulter les horaires de passage de vos bus :');
    console.log('    0. Code arrêt');
    console.log('  OU');
    console.log("    1. Nom de l'arrêt");
    console.log('  OU');
    console.log('    2. Votre ligne');
    console.log('  OU');
    console.log('    3. Quitter');
    console.log('');
}

function exit_input() {
    input("\nPressez n'importe quelle touche pour quitter... ");
}


function main() {
    df_stops = get_stops();
    reponse = null;

    print_log_intro();

    while (reponse != 3) {
        try {
            reponse = Number(input('Faites votre choix parmi les options ci-dessus : '));
            if (reponse == 0) {
                use_case_stop_code(df_stops);
                exit_input();
                break;
            } else if (reponse == 1) {
                use_case_stop_name(df_stops);
                exit_input();
                break;
            } else if (reponse == 2) {
                use_case_choose_line(df_stops);
                exit_input();
                break;

            } else if (reponse == 3) {
                break;

            } else {
                console.log('Entrée non valide');
            }

        } catch ( ValueError as e) {
            console.log(e);
            console.log('Entrée non valide');
        }
    }

    console.log('À bientôt !');
}
