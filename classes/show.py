from psychopy import visual, event, core
import time
import random
import pygame

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
    print key
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


def show(config, win, screen_res, frames_per_sec, blocks, stops_times):
    fixation = visual.TextStim(win, color='black', text='+', height=2 * config['Text_size'])

    arrow_show_time = config['Arrow_show_time'] * frames_per_sec
    stop_show_time = config['Stop_show_time'] * frames_per_sec - 1

    data = list()
    resp_clock = core.Clock()

    for block in blocks:
        for trial in block['trials']:
            # draw fixation
            #
            resp_time = (config['Arrow_show_time'] - config['Resp_time']) * frames_per_sec
            fixation.setAutoDraw(True)
            win.flip()
            time.sleep(config['Fix_time'])
            fixation.setAutoDraw(False)
            win.flip()
            time.sleep(config['Break_between_fix_and_arrow'])
            check_exit()
            event.clearEvents()

            # draw arrow
            #
            win.callOnFlip(resp_clock.reset)
            reaction_time, response = draw_stimulus(win=win, stimulus=trial['arrow'], show_time=arrow_show_time,
                                                    resp_clock=resp_clock, text_size=config['Text_size'],
                                                    screen_res=screen_res, keys=config['Keys'])
            print "arrow", resp_clock.getTime()
            # stop
            #
            if trial['stop'] is not None:
                # break
                stop_wait_time = stops_times[trial['stop'][1]] * frames_per_sec
                reaction_time_2, response_2 = reaction_loop(win=win, show_time=stop_wait_time, keys=config['Keys'],
                                                            resp_clock=resp_clock)
                print 'break', resp_clock.getTime()
                # draw stop
                reaction_time_3, response_3 = draw_stimulus(win=win, stimulus=trial['stop'], show_time=stop_show_time-1,
                                                            resp_clock=resp_clock, text_size=config['Text_size'],
                                                            screen_res=screen_res, keys=config['Keys'])
                # take firs response
                if response is None:
                    reaction_time, response = reaction_time_2, response_2
                    if response is None:
                        reaction_time, response = reaction_time_3, response_3
                        # there was no response - compute rest response time
                        if response is None:
                            resp_time = resp_time - stop_wait_time - stop_show_time

                print "stop", resp_clock.getTime(), trial['stop'][1]

            # Wait for response
            #
            if response is None:
                reaction_time, response = reaction_loop(win=win, show_time=resp_time, keys=config['Keys'],
                                                        resp_clock=resp_clock)
                print "resp", resp_clock.getTime()

            # rest
            #
            jitter = random.random() * config['Rest_time_jitter'] * 2 - config['Rest_time_jitter']
            time.sleep(config['Rest_time'] + jitter)
            win.flip()
            print "rest", resp_clock.getTime()

            # add data
            #
            data.append([trial['arrow'][1], reaction_time, response])

            # update stops_times
            if trial['stop'] is not None:
                wait_time_index = config['Possible_wait_to_stop'].index(stops_times[trial['stop'][1]])
                if response is None:
                    if wait_time_index != len(config['Possible_wait_to_stop']) - 1:
                        stops_times[trial['stop'][1]] = config['Possible_wait_to_stop'][wait_time_index+1]
                else:
                    if wait_time_index != 0:
                        stops_times[trial['stop'][1]] = config['Possible_wait_to_stop'][wait_time_index-1]

        show_info(win=win, file_name=block['text_after_block'], text_size=config['Text_size'],
                  screen_width=screen_res['width'])

    return data
