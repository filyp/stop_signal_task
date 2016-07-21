from psychopy import visual, event, core
import time
import random
import pygame

from classes.load_data import read_text_from_file
from classes.check_exit import check_exit

TRIGGERS = list()


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


def draw_fixation(win, fixation, config):
    fixation.setAutoDraw(True)
    win.flip()
    time.sleep(config['Fix_time'])
    fixation.setAutoDraw(False)
    check_exit()
    win.flip()


def start_stimulus(stimulus):
    if stimulus[0] == 'image':
        stimulus[2].setAutoDraw(True)

    elif stimulus[0] == 'text':
        stimulus[2].setAutoDraw(True)

    elif stimulus[0] == 'sound':
        pygame.init()
        pygame.mixer.music.load(stimulus[2])
        pygame.mixer.music.play()
    else:
        raise Exception("Problems with start stimulus " + stimulus)


def stop_stimulus(stimulus):
    if stimulus[0] == 'image':
        stimulus[2].setAutoDraw(False)

    elif stimulus[0] == 'text':
        stimulus[2].setAutoDraw(False)

    elif stimulus[0] == 'sound':
        pygame.mixer.music.stop()
        pygame.quit()
    else:
        raise Exception("Problems with stop stimulus " + stimulus)


def new_run_trial(win, resp_clock, trial, resp_time, arrow_show_time, stop_show_end, stop_show_start, config):
    reaction_time = None
    response = None

    start_stimulus(stimulus=trial['arrow'])
    check_exit()
    arrow_on = True
    stop_on = None
    event.clearEvents()
    win.callOnFlip(resp_clock.reset)
    win.flip()

    while resp_clock.getTime() < resp_time:
        if arrow_on is True and resp_clock.getTime() > arrow_show_time:
            stop_stimulus(stimulus=trial['arrow'])
            arrow_on = False
        if trial['stop'] is not None:
            if stop_on is None and resp_clock.getTime() > stop_show_start:
                start_stimulus(stimulus=trial['stop'])
                stop_on = True
            if stop_on is True and resp_clock.getTime() > stop_show_end:
                stop_stimulus(stimulus=trial['stop'])
                stop_on = False

        key = event.getKeys(keyList=config['Keys'])
        if key:
            reaction_time = resp_clock.getTime()
            # TRIGGER
            response = key[0]
            break
        check_exit()
        win.flip()

    if arrow_on is True:
        stop_stimulus(stimulus=trial['arrow'])
    if stop_on is True:
        stop_stimulus(stimulus=trial['stop'])

    return reaction_time, response


def update_stops_times(trial, config, response, stops_times):
    if trial['stop'] is not None:
        wait_time_index = config['Possible_wait_to_stop'].index(stops_times[trial['stop'][1]])
        if response is None:
            if wait_time_index != len(config['Possible_wait_to_stop']) - 1:
                stops_times[trial['stop'][1]] = config['Possible_wait_to_stop'][wait_time_index + 1]
        else:
            if wait_time_index != 0:
                stops_times[trial['stop'][1]] = config['Possible_wait_to_stop'][wait_time_index - 1]
    return stops_times


def show(config, win, screen_res, frames_per_sec, blocks, stops_times):
    fixation = visual.TextStim(win, color='black', text='+', height=2 * config['Text_size'])

    # arrow_show_time = int(round(config['Arrow_show_time'] * frames_per_sec)) - 1
    # resp_time = int(round(config['Resp_time'] * frames_per_sec))
    one_frame_time = 1.0/frames_per_sec

    arrow_show_time = config['Arrow_show_time'] - one_frame_time
    resp_time = config['Resp_time'] - one_frame_time

    data = list()
    trial_number = 1
    resp_clock = core.Clock()

    for block in blocks:
        for trial in block['trials']:
            if trial['stop'] is not None:
                # stop_show_start = int(round(stops_times[trial['stop'][1]] * frames_per_sec))
                # stop_show_end = int(round(stop_show_start + config['Stop_show_time'] * frames_per_sec))
                stop_show_start = stops_times[trial['stop'][1]] - one_frame_time
                stop_show_end = stop_show_start + config['Stop_show_time']
            else:
                stop_show_start = None
                stop_show_end = None

            # draw fixation
            draw_fixation(win=win, fixation=fixation, config=config)

            # break between fixation and arrow
            time.sleep(config['Break_between_fix_and_arrow'])
            check_exit()

            # arrow, stop and resp
            reaction_time, response = new_run_trial(win=win, resp_clock=resp_clock, trial=trial, resp_time=resp_time,
                                                    arrow_show_time=arrow_show_time, stop_show_end=stop_show_end,
                                                    stop_show_start=stop_show_start, config=config)

            # rest
            jitter = (2 * random.random() - 1) * config['Rest_time_jitter']
            time.sleep(config['Rest_time'] + jitter)

            # add data
            if trial['stop'] is not None:
                data.append({'Nr': trial_number, 'GO_name': trial['arrow'][1], 'RE_name': response,
                             'RE_time': reaction_time, 'ST_name': trial['stop'][1],
                             'ST_wait_time': stops_times[trial['stop'][1]]})
            else:
                data.append({'Nr': trial_number, 'GO_name': trial['arrow'][1], 'RE_name': response,
                             'RE_time': reaction_time, 'ST_name': None, 'ST_wait_time': None})
            trial_number += 1

            # update stops_times
            stops_times = update_stops_times(trial=trial, config=config, response=response, stops_times=stops_times)

        show_info(win=win, file_name=block['text_after_block'], text_size=config['Text_size'],
                  screen_width=screen_res['width'])

    return data, TRIGGERS
