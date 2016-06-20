#!/usr/bin/env python
# -*- coding: utf-8 -*-

from gooey import Gooey, GooeyParser
from classes.args_to_dict import args_to_dict
import yaml

__author__ = 'ociepkam'


@Gooey(language='english',  # Translations configurable via json
       default_size=(450, 500),  # starting size of the GUI
       required_cols=1,  # number of columns in the "Required" section
       optional_cols=3,  # number of columns in the "Optional" section
       )
def main():
    parser = GooeyParser(description='Create_config')
    parser.add_argument('Experiment_type', default='images', choices=['images', 'text', 'sound'], help='Choice')
    parser.add_argument('Number_of_training_trials', default=4, action='store', type=int, help='Number')
    parser.add_argument('Number_of_experiment_blocks', default=1, action='store', type=int, help='Number')
    parser.add_argument('Number_of_experiment_trials', default=4, action='store', type=int, help='Number')

    parser.add_argument('Arrow_show_time', default=1, action='store', type=int, help='Number')
    parser.add_argument('Stop_show_time', default=1, action='store', type=int, help='Number')
    parser.add_argument('Start_wait_to_stop', default=1, action='store', type=int, help='Number')
    parser.add_argument('Stop_show_time', default=1, action='store', type=int, help='Number')
    parser.add_argument('Resp_time', default=1, action='store', type=int, help='Number')

    parser.add_argument('Fix_time', default=1, action='store', type=int, help='Number')
    parser.add_argument('Break_between_fix_and_arrow', default=1, action='store', type=int, help='Number')

    args = parser.parse_args()

    args_dict = args_to_dict(args)

    with open("docs/config.yaml", 'w') as save_file:
        save_file.write(yaml.dump(args_dict))

if __name__ == '__main__':
    main()