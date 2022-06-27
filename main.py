#!/usr/bin/env python
# -*- coding: utf-8 -*-

import shutil
import os
import copy
import sys

from psychopy import logging
from psychopy.hardware import joystick

from classes.prepare_experiment import prepare_trials, create_stops_times_dict, randomize_buttons
from classes.load_data import load_data, load_config, load_data_in_folders, prepare_words
from classes.screen import create_win
from classes.experiment_info import experiment_info, eeg_info
from classes.ophthalmic_procedure import ophthalmic_procedure
from classes.show import show
from classes.save_data import save_beh, save_triggers
from classes.triggers import create_eeg_port, create_nirs_dev
from classes.show_info import show_info, prepare_buttons_info
from edit_config import config_verification


__author__ = "ociepkam"


def run():
    # Load config
    config_path = sys.argv[1]
    config_verification(config_path)

    config, config_hash = load_config(config_path)  # copy config file to results folder
    experiment_name = os.path.split(config_path)[-1]
    experiment_name = experiment_name.split(".")[0]
    experiment_name = experiment_name + "_" + config_hash
    results_dir = os.path.join("results", experiment_name)
    os.makedirs(results_dir, exist_ok=True)
    shutil.copy2(config_path, results_dir)
    logging.data(f"Experiment name: {experiment_name}")

    eeg_info()
    part_id = experiment_info(config["Observer"])
    part_name = "{}".format(part_id)
    print(part_name)
    # EEG triggers
    if config["Send_EEG_trigg"]:
        port_eeg = create_eeg_port()
    else:
        port_eeg = None
    if config["Send_Nirs_trigg"]:
        port_nirs = create_nirs_dev()
    else:
        port_nirs = None
    triggers_list = list()
    trigger_no = 0

    # screen
    screen_number = config.get("Screen_number", -1)
    win, screen_res, frames_per_sec = create_win(screen_color=config["Screen_color"], screen_number=screen_number)

    # prepare training
    # train_stops, exp_stops = prepare_words(
    #     win=win,
    #     folder_name="stops",
    #     config=config,
    #     screen_res=screen_res,
    #     experiment_version=experiment_version,
    # )
    arrows = load_data(win=win, folder_name="arrows", config=config, screen_res=screen_res)
    stops = load_data(win=win, folder_name="stops", config=config, screen_res=screen_res)

    training_block_1 = prepare_trials(
        number_of_blocks=1,
        stops=stops,
        arrows=arrows,
        number_of_experiment_trials=config["Number_of_training_1_trials"],
        percent_of_trials_with_stop=0,
        messages=[os.path.join("messages", "training_end_1.txt")],
    )

    training_block_2 = prepare_trials(
        number_of_blocks=1,
        stops=stops,
        arrows=arrows,
        number_of_experiment_trials=config["Number_of_training_2_trials"],
        percent_of_trials_with_stop=config["Percent_of_trials_with_stop"],
        messages=[os.path.join("messages", "training_end_2.txt")],
    )

    training_block = training_block_1 + training_block_2

    # prepare experiment
    breaks = [
        os.path.join("messages", "break{}.txt".format(idx + 1))
        for idx in range(config["Number_of_experiment_blocks"])
    ]
    experiment_block = prepare_trials(
        number_of_blocks=config["Number_of_experiment_blocks"],
        number_of_experiment_trials=config["Number_of_experiment_trials"],
        percent_of_trials_with_stop=config["Percent_of_trials_with_stop"],
        stops=stops,
        arrows=arrows,
        messages=breaks,
    )

    stops_times = create_stops_times_dict(
        stops=stops, start_wait_to_stop=config["Start_wait_to_stop"]
    )
    stops_times_train = copy.copy(stops_times)

    # Keys randomization
    if config["Keys_randomization"]:
        config["Keys"] = randomize_buttons(config["Keys"])

    # connect joysitck
    if config["Use_joystick"]:
        if joystick.getNumJoysticks() == 0:
            raise RuntimeError(
                "No joystick found. On linux you need to run this command first: modprobe joydev"
            )
        joy = joystick.Joystick(0)
    else:
        joy = None

    # Run experiment

    # Ophthalmic procedure
    if config["Ophthalmic_procedure"]:
        trigger_no, triggers_list = ophthalmic_procedure(
            win=win,
            send_eeg_triggers=config["Send_EEG_trigg"],
            send_nirs_triggers=config["Send_Nirs_trigg"],
            screen_res=screen_res,
            frames_per_sec=frames_per_sec,
            port_eeg=port_eeg,
            port_nirs=port_nirs,
            trigger_no=trigger_no,
            triggers_list=triggers_list,
            text_size=config["Text_size"],
        )

    # Instruction
    buttons_info = prepare_buttons_info(config["Keys"], config["Keys_description"])
    instructions = sorted([f for f in os.listdir("messages") if f.startswith("instruction")])
    for instruction in instructions:
        show_info(
            win=win,
            file_name=os.path.join("messages", instruction),
            text_size=config["Text_size"],
            screen_width=screen_res["width"],
            insert=buttons_info,
            triggers_list=[],
            part_name=part_name,
            data=[],
            results_dir=results_dir,
        )

    # Training
    beh, _ = show(
        config=config,
        win=win,
        screen_res=screen_res,
        frames_per_sec=frames_per_sec,
        blocks=training_block,
        stops_times=stops_times_train,
        trigger_no=trigger_no,
        triggers_list=[],
        part_id=part_name,
        data=[],
        results_dir=results_dir,
        joy=joy,
    )

    # Experiment
    beh, triggers_list = show(
        config=config,
        win=win,
        screen_res=screen_res,
        frames_per_sec=frames_per_sec,
        blocks=experiment_block,
        stops_times=stops_times,
        port_eeg=port_eeg,
        port_nirs=port_nirs,
        trigger_no=trigger_no,
        triggers_list=triggers_list,
        part_id=part_name,
        data=beh,
        results_dir=results_dir,
        joy=joy,
    )

    # Experiment end
    # show_info(win=win, file_name=os.path.join('messages', 'end.txt'), text_size=config['Text_size'],
    #           screen_width=screen_res['width'], triggers_list=triggers_list, part_name=part_name, data=beh)

    # Save data
    save_beh(data=beh, name=part_name, results_dir=results_dir)
    save_triggers(data=triggers_list, name=part_name, results_dir=results_dir)


run()

# TODO: loggi
# TODO: edit_config ma wczytywac konfiguracje
# TODO: dokumenatcja
