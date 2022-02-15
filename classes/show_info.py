from psychopy import visual, event
import os

from classes.load_data import read_text_from_file
from classes.save_data import save_beh, save_triggers


def show_info(win, file_name, text_size, screen_width, triggers_list, part_name, data, insert=''):
    """
    Clear way to show info message into screen.
    :param win:
    :param file_name:
    :param screen_width:
    :param text_size:
    :param insert: extra text for read_text_from_file
    :return:
    """
    hello_msg = read_text_from_file(file_name, insert=insert)
    hello_msg = visual.TextStim(win=win, antialias=True, font=u'Arial',
                                text=hello_msg, height=text_size,
                                wrapWidth=screen_width, color=u'black',
                                )
    hello_msg.draw()
    win.flip()
    key = event.waitKeys(keyList=['f7', 'return', 'space'])
    if key == ['f7']:
        save_beh(data=data, name=part_name)
        save_triggers(data=triggers_list, name=part_name)
        exit(0)
    win.flip()


def break_info(show_answers_correctness, show_response_time, show_stopped_ratio, show_keys_mapping, answers_correctness,
               response_time, stopped_ratio, keys_mapping):
    extra_info = ""
    if show_answers_correctness:
        file_name = os.path.join('messages', 'answers_correctness.txt')
        extra_info += read_text_from_file(file_name=file_name, insert=answers_correctness) + '\n'
    if show_response_time:
        file_name = os.path.join('messages', 'response_time.txt')
        extra_info += read_text_from_file(file_name=file_name, insert=response_time) + '\n'
    if show_stopped_ratio:
        file_name = os.path.join('messages', 'stopped_ratio.txt')
        extra_info += read_text_from_file(file_name=file_name, insert=stopped_ratio) + '\n'
    if show_keys_mapping:
        extra_info += keys_mapping + '\n'

    return extra_info


def prepare_buttons_info(dict_to_show, keys_text_mapping):
    new_dict = dict()
    for key in dict_to_show:
        key_type = key.split('_')[0]
        new_dict[key_type] = dict_to_show[key]

    info_to_show = ''
    for key in new_dict:
        info_to_show += '{} - {}\n'.format(key, keys_text_mapping[new_dict[key]])

    return info_to_show[:-1]
