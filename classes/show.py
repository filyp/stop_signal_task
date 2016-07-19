from psychopy import visual, event, core
import time
import random

from classes.load_data import read_text_from_file
from classes.check_exit import check_exit


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


def reaction_loop(win, show_time, keys, resp_clock):
    reaction_time = None
    response = None
    for _ in range(show_time):
        check_exit()
        win.flip()
        keys = event.getKeys(keyList=keys)
        if keys:
            reaction_time = resp_clock.getTime()
            # TRIGGER
            response = keys[0]
            break
    return reaction_time, response


def show(config, win, screen_res, frames_per_sec, blocks):
    fixation = visual.TextStim(win, color='black', text='+', height=2 * config['Text_size'])

    arrow_show_time = config['Arrow_show_time'] * frames_per_sec
    resp_time = (config['Arrow_show_time'] - config['Resp_time']) * frames_per_sec

    data = list()
    resp_clock = core.Clock()

    for block in blocks:
        for trial in block['trials']:
            # draw fixation
            fixation.setAutoDraw(True)
            win.flip()
            time.sleep(config['Fix_time'])
            fixation.setAutoDraw(False)
            check_exit()
            event.clearEvents()

            # draw arrow
            trial['arrow'][2].setAutoDraw(True)
            win.callOnFlip(resp_clock.reset)
            # TRIGGER
            reaction_time, response = reaction_loop(win=win, show_time=arrow_show_time, keys=config['Keys'],
                                                    resp_clock=resp_clock)
            trial['arrow'][2].setAutoDraw(False)
            win.flip()

            # stop
            if trial['stop'] is not None:
                # draw stop
                print "rysuj"
            else:
                # there is no stop. Wait for resp
                reaction_time, response = reaction_loop(win=win, show_time=resp_time, keys=config['Keys'],
                                                        resp_clock=resp_clock)

            # rest
            jitter = random.random() * config['Rest_time_jitter'] * 2 - config['Rest_time_jitter']
            time.sleep(config['Rest_time'] + jitter)
            win.flip()
            data.append([reaction_time, response])
        show_info(win=win, file_name=block['text_after_block'], text_size=config['Text_size'],
                  screen_width=screen_res['width'])

    return data
