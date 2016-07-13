#!/usr/bin/env python
# -*- coding: utf-8 -*-

from classes.prepare_experiment import prepare_trials
from classes.load_data import load_data, load_config
from classes.screen import create_win
from classes.experiment_info import experiment_info
from classes.ophthalmic_procedure import ophthalmic_procedure

__author__ = 'ociepkam'


def run():
    config = load_config()
    part_id, observer_id, date = experiment_info(config['Observer'])

    # screen
    win, screen_res, frames_per_sec = create_win(screen_color=config['screen_color'])

    # prepare experiment
    stops = load_data(win=win, folder_name="stops")
    arrows = load_data(win=win, folder_name="arrows")

    training_block, experiment_block = prepare_trials(number_of_blocks=config['Number_of_experiment_blocks'],
                                                      number_of_experiment_trials=config['Number_of_experiment_trials'],
                                                      number_of_training_trials=config['Number_of_training_trials'],
                                                      number_of_stop_types=len(stops),
                                                      percent_of_trials_with_stop=config['Percent_of_trials_with_stop'],
                                                      number_of_arrows=len(arrows))

    if config['Ophthalmic_procedure']:
        ophthalmic_procedure(win=win, send_triggers=False, screen_res=screen_res, frames_per_sec=frames_per_sec)
run()

"""
TODO:
stop w postaci wyrazu
strzalka w postaci wyrazu
triggery
"""
