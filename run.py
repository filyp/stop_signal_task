#!/usr/bin/env python
# -*- coding: utf-8 -*-

from classes.prepare_experiment import prepare_trials
from classes.load_data import load_data, load_config
from classes.screen import create_win
from classes.experiment_info import experiment_info
from classes.ophthalmic_procedure import ophthalmic_procedure
from classes.show import show_info, show

from psychopy import visual
import os

import cgitb

# cgitb.enable(format="text")

__author__ = 'ociepkam'


def run():
    # Prepare experiment
    config = load_config()
    part_id, observer_id, date = experiment_info(config['Observer'])

    # screen
    win, screen_res, frames_per_sec = create_win(screen_color=config['Screen_color'])
    fixation_cross = visual.TextStim(win, color='black', text='+', height=2 * config['Text_size'])

    # prepare experiment
    stops = load_data(win=win, folder_name="stops")
    arrows = load_data(win=win, folder_name="arrows")

    training_block, experiment_block = prepare_trials(number_of_blocks=config['Number_of_experiment_blocks'],
                                                      number_of_experiment_trials=config['Number_of_experiment_trials'],
                                                      number_of_training_trials=config['Number_of_training_trials'],
                                                      stops=stops,
                                                      percent_of_trials_with_stop=config['Percent_of_trials_with_stop'],
                                                      arrows=arrows)

    # Run experiment
    # Ophthalmic procedure
    if config['Ophthalmic_procedure']:
        ophthalmic_procedure(win=win, send_triggers=False, screen_res=screen_res, frames_per_sec=frames_per_sec)

    # Instruction
    show_info(win=win, file_name=os.path.join('messages', 'instruction.txt'), text_size=config['Text_size'],
              screen_width=screen_res['width'])

    # Training
    show(training_block)

    # After training
    show_info(win=win, file_name=os.path.join('messages', 'training_end.txt'), text_size=config['Text_size'],
              screen_width=screen_res['width'])

    # Experiment
    for idx, block in enumerate(experiment_block):
        show(block)
        show_info(win=win, file_name=os.path.join('messages', 'break{}.txt'.format(idx+1)), text_size=config['Text_size'],
                  screen_width=screen_res['width'])

    # Experiment end
    show_info(win=win, file_name=os.path.join('messages', 'end.txt'), text_size=config['Text_size'],
              screen_width=screen_res['width'])

run()

# TODO: triggery
# TODO: wyswietlanie
