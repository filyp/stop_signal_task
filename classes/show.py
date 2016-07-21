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


def reaction_loop(win, show_time, keys, resp_clock):
    reaction_time = None
    response = None
    for _ in range(show_time):
        check_exit()
        win.flip()
        key = event.getKeys(keyList=keys)
        if key:
            reaction_time = resp_clock.getTime()
            # TRIGGER
            response = key[0]
            break
    return reaction_time, response


def draw_fixation(win, fixation, config):
    fixation.setAutoDraw(True)
    win.flip()
    time.sleep(config['Fix_time'])
    fixation.setAutoDraw(False)
    check_exit()
    win.flip()


def draw_image(win, image, show_time, resp_clock, keys):
    image[2].setAutoDraw(True)
    # TRIGGER
    reaction_time, response = reaction_loop(win=win, show_time=show_time, keys=keys,
                                            resp_clock=resp_clock)
    image[2].setAutoDraw(False)
    win.flip()
    return reaction_time, response


def draw_text(win, text, show_time, resp_clock, text_size, screen_res, keys):
    word = visual.TextStim(win=win, antialias=True, font=u'Arial',
                           text=text[2], height=text_size,
                           wrapWidth=screen_res['width'], color=u'black',
                           alignHoriz='center', alignVert='center')
    word.setAutoDraw(True)
    # TRIGGER
    reaction_time, response = reaction_loop(win=win, show_time=show_time, keys=keys,
                                            resp_clock=resp_clock)
    word.setAutoDraw(False)
    win.flip()
    return reaction_time, response


def draw_sound(win, sound, show_time, resp_clock, keys):
    pygame.init()
    pygame.mixer.music.load(sound[2])
    pygame.mixer.music.play()
    # TRIGGER
    reaction_time, response = reaction_loop(win=win, show_time=show_time, keys=keys,
                                            resp_clock=resp_clock)
    pygame.mixer.music.stop()
    pygame.quit()
    win.flip()
    return reaction_time, response


def draw_stimulus(win, stimulus, show_time, resp_clock, text_size, screen_res, keys):
    reaction_time = None
    response = None

    if stimulus[0] == 'image':
        reaction_time, response = draw_image(win=win, image=stimulus, show_time=show_time, resp_clock=resp_clock,
                                             keys=keys)
    elif stimulus[0] == 'text':
        reaction_time, response = draw_text(win=win, text=stimulus, show_time=show_time, resp_clock=resp_clock,
                                            text_size=text_size, screen_res=screen_res, keys=keys)
    elif stimulus[0] == 'sound':
        reaction_time, response = draw_sound(win=win, sound=stimulus, show_time=show_time, resp_clock=resp_clock,
                                             keys=keys)

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

    arrow_show_time = config['Arrow_show_time'] * frames_per_sec
    stop_show_time = config['Stop_show_time'] * frames_per_sec - 1

    data = list()
    trial_number = 1
    resp_clock = core.Clock()

    for block in blocks:
        for trial in block['trials']:
            resp_time = (config['Resp_time'] - config['Arrow_show_time']) * frames_per_sec

            # draw fixation
            draw_fixation(win=win, fixation=fixation, config=config)

            # break between fixation and arrow
            time.sleep(config['Break_between_fix_and_arrow'])
            check_exit()

            event.clearEvents()

            # draw arrow
            #
            win.callOnFlip(resp_clock.reset)
            reaction_time, response = draw_stimulus(win=win, stimulus=trial['arrow'], show_time=arrow_show_time,
                                                    resp_clock=resp_clock, text_size=config['Text_size'],
                                                    screen_res=screen_res, keys=config['Keys'])
            # stop
            #
            if trial['stop'] is not None:
                # break
                stop_wait_time = stops_times[trial['stop'][1]] * frames_per_sec
                reaction_time_2, response_2 = reaction_loop(win=win, show_time=stop_wait_time, keys=config['Keys'],
                                                            resp_clock=resp_clock)

                # draw stop
                reaction_time_3, response_3 = draw_stimulus(win=win, stimulus=trial['stop'],
                                                            show_time=stop_show_time - 1,
                                                            resp_clock=resp_clock, text_size=config['Text_size'],
                                                            screen_res=screen_res, keys=config['Keys'])
                # take firs response
                if response is None:
                    reaction_time, response = reaction_time_2, response_2
                    if response is None:
                        reaction_time, response = reaction_time_3, response_3
                        # there was no response - compute rest response time
                        if response is None:
                            resp_time = resp_time - stop_show_time - stop_wait_time

            # Wait for response
            #
            if response is None:
                reaction_time, response = reaction_loop(win=win, show_time=resp_time, keys=config['Keys'],
                                                        resp_clock=resp_clock)

            # rest
            #
            jitter = (2 * random.random() - 1) * config['Rest_time_jitter']
            time.sleep(config['Rest_time'] + jitter)

            # add data
            #
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
