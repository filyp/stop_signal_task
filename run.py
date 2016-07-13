#!/usr/bin/env python
# -*- coding: utf-8 -*-


from os.path import join
import yaml
from psychopy import visual, event

from classes.prepare_experiment import prepare_trials
from classes.load_data import load_data

__author__ = 'ociepkam'


def load_config():
    with open(join("docs", "config.yaml")) as yaml_file:
        doc = yaml.load(yaml_file)
    return doc


def run():
    config = load_config()

    win = visual.Window(fullscr=True, winType='pyglet', units='deg',
                        size=[1920, 1080], monitor='testMonitor',
                        color=u'black')
    event.Mouse(visible=False, newPos=None, win=win)

    training_block, experiment_block = prepare_trials(number_of_blocks=config['Number_of_experiment_blocks'],
                                                      number_of_experiment_trials=config['Number_of_experiment_trials'],
                                                      number_of_training_trials=config['Number_of_training_trials'],
                                                      number_of_stop_types=2,
                                                      percent_of_trials_with_stop=config['Percent_of_trials_with_stop'],
                                                      number_of_arrows=2)

    stops = load_data(win=win, folder_name="stops")
    arrows = load_data(win=win, folder_name="arrows")


run()


"""
TODO:
stop w postaci wyrazu
strzalka w postaci wyrazu
"""