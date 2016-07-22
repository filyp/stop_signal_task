#!/usr/bin/env python
# -*- coding: utf-8 -*-

from classes.load_data import load_data_names, load_config

from psychopy import gui
import yaml

__author__ = 'ociepkam'

CONFIG_KEYS = [
    # Observer info
    'Observer',
    # Experiment length
    'Number_of_training_trials', 'Number_of_experiment_blocks', 'Number_of_experiment_trials',
    # Trial info
    'Arrow_show_time', 'Percent_of_trials_with_stop', 'Start_wait_to_stop', 'Stop_show_time', 'Resp_time',
    'Rest_time', 'Rest_time_jitter',
    # Triggers info
    'Ophthalmic_procedure', 'Send_EEG_trigg', 'Send_Nirs_trigg',
    # View info
    'Text_size', 'Fix_time', 'Break_between_fix_and_arrow', 'Screen_color',
    # Break info
    'Show_answers_correctness', 'Show_response_time', 'Show_stopped_ratio'
]


def config_verification():
    config = load_config()

    # All elements
    for key in CONFIG_KEYS:
        assert key in config.keys(), 'No ' + key + ' in config'

    assert config['Rest_time_jitter'] <= config['Rest_time'], 'Rest_time_jitter is longer than Rest_time'
    assert config['Number_of_experiment_blocks'] <= config['Number_of_experiment_trials'], 'More blocks than trials'


def main():
    my_dlg = gui.Dlg(title="SST - config")
    my_dlg.addText('Observer info')
    my_dlg.addField('Observer')

    my_dlg.addText('Experiment length')
    my_dlg.addField('Number_of_training_trials', 4)
    my_dlg.addField('Number_of_experiment_blocks', 1)
    my_dlg.addField('Number_of_experiment_trials', 4)

    my_dlg.addText('Trial info')
    my_dlg.addField('Arrow_show_time', 1)
    my_dlg.addField('Percent_of_trials_with_stop', 25)
    my_dlg.addField('Start_wait_to_stop', 1)
    my_dlg.addField('Stop_show_time', 1)
    my_dlg.addField('Resp_time', 2)
    my_dlg.addField('Rest_time', 1)
    my_dlg.addField('Rest_time_jitter', 1)

    my_dlg.addText('Triggers info')
    my_dlg.addField('Ophthalmic_procedure', choices=['False', 'True'])
    my_dlg.addField('Send_EEG_trigg', choices=['False', 'True'])
    my_dlg.addField('Send_Nirs_trigg', choices=['False', 'True'])

    my_dlg.addText('View info')
    my_dlg.addField('Text_size', 40)
    my_dlg.addField('Fix_time', 1)
    my_dlg.addField('Break_between_fix_and_arrow', 1)
    my_dlg.addField('Screen_color', 'Gainsboro')

    my_dlg.addText('Break info')
    my_dlg.addField('Show_answers_correctness', choices=['False', 'True'])
    my_dlg.addField('Show_response_time', choices=['False', 'True'])
    my_dlg.addField('Show_stopped_ratio', choices=['False', 'True'])

    my_dlg.show()
    if not my_dlg.OK:
        exit(1)

    if len(CONFIG_KEYS) != len(my_dlg.data):
        raise Exception("Problems with config")

    args_dict = dict()
    for idx, key in enumerate(CONFIG_KEYS):
        if isinstance(my_dlg.data[idx], unicode):
            my_dlg.data[idx] = str(my_dlg.data[idx])
        if my_dlg.data[idx] == 'False':
            my_dlg.data[idx] = False
        elif my_dlg.data[idx] == 'True':
            my_dlg.data[idx] = True
        args_dict[key] = my_dlg.data[idx]

    args_dict['Possible_wait_to_stop'] = [args_dict['Start_wait_to_stop']]

    arrows_names = load_data_names('arrows')
    arrows_names = sorted(arrows_names)

    if len(arrows_names) == 0:
        keys = []
    elif len(arrows_names) == 2:
        keys = {arrows_names[0]: 'lctrl', arrows_names[1]: 'rctrl'}
    else:
        keys = dict()
        for arrow in arrows_names:
            keys[arrow] = 'space'

    args_dict['Keys'] = keys

    with open("docs/config.yaml", 'w') as save_file:
        save_file.write(yaml.dump(args_dict))

    config_verification()

if __name__ == '__main__':
    main()
