#!/usr/bin/env python
# -*- coding: utf-8 -*-

from gooey import Gooey, GooeyParser
from os.path import join

from classes.args_to_dict import args_to_dict
import yaml

__author__ = 'ociepkam'


def load_config():
    with open(join("docs", "config.yaml")) as yaml_file:
        doc = yaml.load(yaml_file)
    return doc


@Gooey(language='english',  # Translations configurable via json
       default_size=(450, 500),  # starting size of the GUI
       required_cols=1,  # number of columns in the "Required" section
       optional_cols=3,  # number of columns in the "Optional" section
       )
def run():
    parser = GooeyParser(description='Run_experiment')
    parser.add_argument('Participant_ID', type=str)
    parser.add_argument('Participant_Sex', default='M', choices=['M', 'F'])
    parser.add_argument('Observer', type=str)
    parser.add_argument('EEG_connected', default='0', choices=['1', '0'], help='Choice')
    parser.add_argument('NIRS_connected', default='0', choices=['1', '0'], help='Choice')

    args = parser.parse_args()

    args_dict = args_to_dict(args)


#if __name__ == '__main__':
#    run()

load_config()