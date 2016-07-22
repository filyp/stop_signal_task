from psychopy import visual, event
import os

from classes.load_data import read_text_from_file


def show_info(win, file_name, text_size, screen_width, insert=''):
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
                                alignHoriz='center', alignVert='center')
    hello_msg.draw()
    win.flip()
    key = event.waitKeys(keyList=['f7', 'return', 'space'])
    if key == ['f7']:
        exit(0)
    win.flip()


def break_info(show_answers_correctness, show_response_time, show_stopped_ratio, answers_correctness, response_time,
               stopped_ratio):
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

    return extra_info
