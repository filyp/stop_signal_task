#!/usr/bin/env python
# -*- coding: utf-8 -*-

from classes.prepare_experiment import prepare_trials, create_stops_times_dict, randomize_buttons
from classes.load_data import load_data, load_config
from classes.screen import create_win
from classes.experiment_info import experiment_info
from classes.ophthalmic_procedure import ophthalmic_procedure
from classes.show import show
from classes.save_data import save_beh, save_triggers
from classes.triggers import create_eeg_port, create_nirs_dev
from classes.show_info import show_info, prepare_buttons_info
from edit_config import config_verification

import os

# import cgitb
# cgitb.enable(format="text")

__author__ = 'ociepkam'


def run():
    # Prepare experiment
    config_verification()
    config = load_config()
    part_id, sex, age, observer_id, date = experiment_info(config['Observer'])

    # EEG triggers
    if config['Send_EEG_trigg']:
        port_eeg = create_eeg_port()
    else:
        port_eeg = None
    if config['Send_Nirs_trigg']:
        port_nirs = create_nirs_dev()
    else:
        port_nirs = None
    triggers_list = list()
    trigger_no = 0

    # screen
    win, screen_res, frames_per_sec = create_win(screen_color=config['Screen_color'])

    # prepare experiment
    stops = load_data(win=win, folder_name="stops", config=config, screen_res=screen_res)
    arrows = load_data(win=win, folder_name="arrows", config=config, screen_res=screen_res)

    training_block, experiment_block = prepare_trials(number_of_blocks=config['Number_of_experiment_blocks'],
                                                      number_of_experiment_trials=config['Number_of_experiment_trials'],
                                                      number_of_training_trials=config['Number_of_training_trials'],
                                                      stops=stops,
                                                      percent_of_trials_with_stop=config['Percent_of_trials_with_stop'],
                                                      arrows=arrows)

    stops_times = create_stops_times_dict(stops=stops, start_wait_to_stop=config['Start_wait_to_stop'])

    # Keys randomization
    if config['Keys_randomization']:
        config['Keys'] = randomize_buttons(config['Keys'])

    # Run experiment
    # Ophthalmic procedure
    if config['Ophthalmic_procedure']:
        trigger_no, triggers_list = ophthalmic_procedure(win=win, send_eeg_triggers=config['Send_EEG_trigg'],
                                                         send_nirs_triggers=config['Send_Nirs_trigg'],
                                                         screen_res=screen_res, frames_per_sec=frames_per_sec,
                                                         port_eeg=port_eeg, port_nirs=port_nirs, trigger_no=trigger_no,
                                                         triggers_list=triggers_list, text_size=config['Text_size'])

    # Instruction
    buttons_info = prepare_buttons_info(config['Keys'])
    instructions = sorted([f for f in os.listdir('messages') if f.startswith('instruction')])
    for instruction in instructions:
        show_info(win=win, file_name=os.path.join('messages', instruction), text_size=config['Text_size'],
                  screen_width=screen_res['width'], insert=buttons_info)

    # Training
    show(config=config, win=win, screen_res=screen_res, frames_per_sec=frames_per_sec,
         blocks=training_block, stops_times=stops_times, trigger_no=trigger_no,
         triggers_list=triggers_list)

    # Experiment
    beh, triggers_list = show(config=config, win=win, screen_res=screen_res, frames_per_sec=frames_per_sec,
                              blocks=experiment_block, stops_times=stops_times, port_eeg=port_eeg, port_nirs=port_nirs,
                              trigger_no=trigger_no, triggers_list=triggers_list)

    # Save data
    save_beh(data=beh, name=part_id)
    save_triggers(data=triggers_list, name=part_id)

    # Experiment end
    show_info(win=win, file_name=os.path.join('messages', 'end.txt'), text_size=config['Text_size'],
              screen_width=screen_res['width'])


run()

# TODO: loggi

# TODO: dokumenatcja
