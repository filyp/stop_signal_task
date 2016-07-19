#!/usr/bin/env python
# -*- coding: utf-8 -*-

from gooey import Gooey, GooeyParser
import yaml

__author__ = 'ociepkam'


def args_to_dict(args):

    args = str(args).split('(')[1][:-1]
    args_list = args.split(", ")
    args_dict = {}
    for arg in args_list:
        arg_param = arg.split("=")
        try:
            args_dict[arg_param[0]] = int(arg_param[1])
        except:
            temp = arg_param[1].split('\'')
            temp = [word for word in temp if word is not '']
            args_dict[arg_param[0]] = temp[0]
            if temp[0] in ('True', 'False'):
                args_dict[arg_param[0]] = bool(args_dict[arg_param[0]])
    return args_dict


@Gooey(language='english',  # Translations configurable via json
       default_size=(550, 500),  # starting size of the GUI
       required_cols=1,  # number of columns in the "Required" section
       optional_cols=3,  # number of columns in the "Optional" section
       )
def main():
    parser = GooeyParser(description='Create_config')
    parser.add_argument('Observer', action='store', help='Observer id')
    parser.add_argument('Number_of_training_trials', default=4, action='store', type=int, help='Number')
    parser.add_argument('Number_of_experiment_blocks', default=1, action='store', type=int, help='Number')
    parser.add_argument('Number_of_experiment_trials', default=4, action='store', type=int, help='Number')
    parser.add_argument('Percent_of_trials_with_stop', default=25, action='store', type=int, help='Number')

    parser.add_argument('Arrow_show_time', default=1, action='store', type=int, help='Number')
    parser.add_argument('Stop_show_time', default=1, action='store', type=int, help='Number')
    parser.add_argument('Start_wait_to_stop', default=1, action='store', type=int, help='Number')
    parser.add_argument('Stop_show_time', default=1, action='store', type=int, help='Number')
    parser.add_argument('Resp_time', default=1, action='store', type=int, help='Number')

    parser.add_argument('Text_size', default=70, action='store', type=int, help='Number')
    parser.add_argument('Fix_time', default=1, action='store', type=int, help='Number')
    parser.add_argument('Break_between_fix_and_arrow', default=1, action='store', type=int, help='Number')
    parser.add_argument('Rest_time', default=1, action='store', type=int, help='Number')
    parser.add_argument('Rest_time_jitter', default=1, action='store', type=int, help='Number')

    parser.add_argument('Screen_color', default='Gainsboro', action='store', help='screen_color')

    parser.add_argument('Ophthalmic_procedure', default='True', choices=['True', 'False'], help='Choice')


    args = parser.parse_args()

    args_dict = args_to_dict(args)
    args_dict['Keys'] = ['lctrl', 'rctrl']

    with open("docs/config.yaml", 'w') as save_file:
        save_file.write(yaml.dump(args_dict))

if __name__ == '__main__':
    main()
