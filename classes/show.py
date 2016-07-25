from psychopy import visual, event, core
import time
import random
import pygame

from classes.show_info import show_info, break_info, prepare_buttons_info
from classes.check_exit import check_exit
from classes.triggers import prepare_trigger, TriggerTypes, send_trigger, prepare_trigger_name

PORT_EEG = None
PORT_NIRS = None
TRIGGERS_LIST = list()
TRIGGER_NO = 0


def draw_fixation(win, fixation, config):
    fixation.setAutoDraw(True)
    win.flip()
    time.sleep(config['Fix_time'])
    fixation.setAutoDraw(False)
    check_exit()
    win.flip()


def start_stimulus(win, stimulus, send_eeg_triggers, send_nirs_triggers):
    global TRIGGER_NO, TRIGGERS_LIST

    if stimulus[0] == 'image':
        stimulus[2].setAutoDraw(True)
        win.flip()
        send_trigger(port_eeg=PORT_EEG, port_nirs=PORT_NIRS, trigger_no=TRIGGER_NO,
                     send_eeg_triggers=send_eeg_triggers,
                     send_nirs_triggers=send_nirs_triggers)

    elif stimulus[0] == 'text':
        stimulus[2].setAutoDraw(True)
        win.flip()
        send_trigger(port_eeg=PORT_EEG, port_nirs=PORT_NIRS, trigger_no=TRIGGER_NO,
                     send_eeg_triggers=send_eeg_triggers,
                     send_nirs_triggers=send_nirs_triggers)

    elif stimulus[0] == 'sound':
        pygame.init()
        pygame.mixer.music.load(stimulus[2])
        win.flip()
        pygame.mixer.music.play()
        send_trigger(port_eeg=PORT_EEG, port_nirs=PORT_NIRS, trigger_no=TRIGGER_NO,
                     send_eeg_triggers=send_eeg_triggers,
                     send_nirs_triggers=send_nirs_triggers)
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


def run_trial(win, resp_clock, trial, resp_time, arrow_show_time, stop_show_end, stop_show_start, config,
              real_stop_show_start):
    global PORT_EEG, TRIGGER_NO, TRIGGERS_LIST

    reaction_time = None
    response = None
    trigger_name = prepare_trigger_name(trial=trial, stop_show_start=real_stop_show_start)
    TRIGGER_NO, TRIGGERS_LIST = prepare_trigger(trigger_type=TriggerTypes.GO, trigger_no=TRIGGER_NO,
                                                triggers_list=TRIGGERS_LIST, trigger_name=trigger_name)
    start_stimulus(win=win, stimulus=trial['arrow'], send_eeg_triggers=config['Send_EEG_trigg'],
                   send_nirs_triggers=config['Send_Nirs_trigg'])
    check_exit()
    arrow_on = True
    stop_on = None
    event.clearEvents()
    win.callOnFlip(resp_clock.reset)
    win.flip()

    while resp_clock.getTime() < resp_time:
        change = False
        if arrow_on is True and resp_clock.getTime() > arrow_show_time:
            stop_stimulus(stimulus=trial['arrow'])
            arrow_on = False
            change = True
        if trial['stop'] is not None:
            if stop_on is None and resp_clock.getTime() > stop_show_start:
                TRIGGER_NO, TRIGGERS_LIST = prepare_trigger(trigger_type=TriggerTypes.ST, trigger_no=TRIGGER_NO,
                                                            triggers_list=TRIGGERS_LIST, trigger_name=trigger_name)
                start_stimulus(win=win, stimulus=trial['stop'], send_eeg_triggers=config['Send_EEG_trigg'],
                               send_nirs_triggers=config['Send_Nirs_trigg'])
                stop_on = True
                change = True
            if stop_on is True and resp_clock.getTime() > stop_show_end:
                stop_stimulus(stimulus=trial['stop'])
                stop_on = False
                change = True

        key = event.getKeys(keyList=config['Keys'].values())
        if key:
            reaction_time = resp_clock.getTime()
            TRIGGER_NO, TRIGGERS_LIST = prepare_trigger(trigger_type=TriggerTypes.RE, trigger_no=TRIGGER_NO,
                                                        triggers_list=TRIGGERS_LIST, trigger_name=trigger_name)
            if config['Send_EEG_trigg']:
                send_trigger(port_eeg=PORT_EEG, port_nirs=PORT_NIRS, trigger_no=TRIGGER_NO,
                             send_eeg_triggers=config['Send_EEG_trigg'],
                             send_nirs_triggers=config['Send_Nirs_trigg'])
            response = key[0]
            break
        check_exit()
        if change is False:
            win.flip()

    if arrow_on is True:
        stop_stimulus(stimulus=trial['arrow'])
    if stop_on is True:
        stop_stimulus(stimulus=trial['stop'])

    # Add response to all trial triggers
    if response is not None:
        TRIGGERS_LIST[-1] = (TRIGGERS_LIST[-1][0], TRIGGERS_LIST[-1][1][:-1] + response)
        TRIGGERS_LIST[-2] = (TRIGGERS_LIST[-2][0], TRIGGERS_LIST[-2][1][:-1] + response)
        if TRIGGERS_LIST[-2][1].startswith('ST'):
            TRIGGERS_LIST[-3] = (TRIGGERS_LIST[-3][0], TRIGGERS_LIST[-3][1][:-1] + response)

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


def show(config, win, screen_res, frames_per_sec, blocks, stops_times, trigger_no, triggers_list,
         port_eeg=None, port_nirs=None):
    global PORT_EEG, PORT_NIRS, TRIGGERS_LIST, TRIGGER_NO
    PORT_EEG = port_eeg
    PORT_NIRS = port_nirs
    TRIGGERS_LIST = triggers_list
    TRIGGER_NO = trigger_no

    fixation = visual.TextStim(win, color='black', text='+', height=2 * config['Text_size'])

    one_frame_time = 1.0 / frames_per_sec

    arrow_show_time = config['Arrow_show_time'] - one_frame_time
    resp_time = config['Resp_time'] - one_frame_time

    data = list()
    trial_number = 1
    resp_clock = core.Clock()

    for block in blocks:
        all_reactions_times = 0.
        no_reactions = 0.
        answers_correctness = 0.
        stopped_trials = 0.
        not_stopped_trials = 0.
        for trial in block['trials']:
            if trial['stop'] is not None:
                real_stop_show_start = stops_times[trial['stop'][1]]
                stop_show_start = real_stop_show_start - one_frame_time
                stop_show_end = stop_show_start + config['Stop_show_time']
            else:
                real_stop_show_start = None
                stop_show_start = None
                stop_show_end = None

            # draw fixation
            draw_fixation(win=win, fixation=fixation, config=config)

            # break between fixation and arrow
            time.sleep(config['Break_between_fix_and_arrow'])
            check_exit()

            # arrow, stop and resp
            reaction_time, response = run_trial(win=win, resp_clock=resp_clock, trial=trial, resp_time=resp_time,
                                                arrow_show_time=arrow_show_time, stop_show_end=stop_show_end,
                                                stop_show_start=stop_show_start, config=config,
                                                real_stop_show_start=real_stop_show_start)

            # rest
            jitter = (2 * random.random() - 1) * config['Rest_time_jitter']
            time.sleep(config['Rest_time'] + jitter)

            # add data
            if trial['stop'] is not None:
                data.append({'Nr': trial_number,
                             'GO_type': trial['arrow'][0], 'GO_name': trial['arrow'][1],
                             'RE_key': response, 'RE_time': reaction_time, 'RE_true': config['Keys'][trial['arrow'][1]],
                             'ST_type': trial['stop'][0], 'ST_name': trial['stop'][1],
                             'ST_wait_time': stops_times[trial['stop'][1]]})
            else:
                data.append({'Nr': trial_number,
                             'GO_type': trial['arrow'][0], 'GO_name': trial['arrow'][1],
                             'RE_key': response, 'RE_true': config['Keys'][trial['arrow'][1]], 'RE_time': reaction_time,
                             'ST_type': None, 'ST_name': None, 'ST_wait_time': None})
            trial_number += 1

            # break info
            if reaction_time is not None:
                all_reactions_times += reaction_time
                if response == config['Keys'][trial['arrow'][1]]:
                    answers_correctness += 1
            else:
                if trial['stop'] is not None:
                    no_reactions += 1
                else:
                    all_reactions_times += config['Resp_time']

            if trial['stop'] is not None:
                if reaction_time is not None:
                    not_stopped_trials += 1
                else:
                    stopped_trials += 1

            # update stops_times
            stops_times = update_stops_times(trial=trial, config=config, response=response, stops_times=stops_times)

        # break info

        try:
            all_reactions_times /= (len(block['trials']) - no_reactions)
            all_reactions_times = round(all_reactions_times, 2)
            answers_correctness /= (len(block['trials']) - no_reactions)
            answers_correctness = round(100 * answers_correctness, 2)
        except:
            all_reactions_times = 'No answers!'
            answers_correctness = 'No answers!'
        try:
            stopped_ratio = stopped_trials / (not_stopped_trials + stopped_trials)
            stopped_ratio = round(100 * stopped_ratio, 2)
        except:
            stopped_ratio = 'No stops!'

        keys_mapping = prepare_buttons_info(config['Keys'])

        break_extra_info = break_info(show_answers_correctness=config['Show_answers_correctness'],
                                      show_response_time=config['Show_response_time'],
                                      show_stopped_ratio=config['Show_stopped_ratio'],
                                      show_keys_mapping=config['Show_keys_mapping'],
                                      answers_correctness=str(answers_correctness) + '%',
                                      response_time=str(all_reactions_times) + 's',
                                      stopped_ratio=str(stopped_ratio) + '%',
                                      keys_mapping=keys_mapping)
        show_info(win=win, file_name=block['text_after_block'], text_size=config['Text_size'],
                  screen_width=screen_res['width'], insert=break_extra_info)

    return data, TRIGGERS_LIST
