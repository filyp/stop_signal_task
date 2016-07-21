from psychopy import visual, logging
import time
import os

from classes.load_data import read_text_from_file
from classes.check_exit import check_exit
from classes.triggers import prepare_trigger, TriggerTypes, send_trigger
from classes.experiment_info import TEXT_SIZE


def ophthalmic_procedure(win, send_triggers, screen_res, frames_per_sec, port, trigger_no, triggers_list,
                         vis_offset=60, secs_of_msg=5, secs_of_blinks=9, secs_of_saccades=9):
    """
    :param triggers_list:
    :param trigger_no:
    :param port:
    :param frames_per_sec:
    :param screen_res:
    :param win:
    :param send_triggers:
    :param vis_offset: No of pixels of margin between fixation crosses and screen border
    :param secs_of_msg:
    :param secs_of_blinks:
    :param secs_of_saccades:
    :return:
    """
    logging.info('Starting ophthalmic procedure... ')
    # prepare stim's
    ophthalmic_info = read_text_from_file(os.path.join('.', 'messages', 'ophthalmic_instruction.txt'))
    corners_info = read_text_from_file(os.path.join('.', 'messages', 'ophthalmic_corners.txt'))

    ophthalmic_info = visual.TextStim(win=win, font=u'Arial', text=ophthalmic_info, height=TEXT_SIZE,
                                      wrapWidth=screen_res['width'], color=u'black')
    corners_info = visual.TextStim(win=win, font=u'Arial', text=corners_info, height=TEXT_SIZE,
                                   wrapWidth=screen_res['width'], color=u'black')
    # crosses are located in corners
    crosses = [[x, y] for x in [-screen_res['width'] / 2 + vis_offset, screen_res['width'] / 2 - vis_offset] for y in
               [-screen_res['height'] / 2 + vis_offset, screen_res['height'] / 2 - vis_offset]]
    crosses = [visual.TextStim(win=win, text=u'+', height=3 * TEXT_SIZE, color=u'black', pos=pos) for pos in crosses]

    ophthalmic_info.setAutoDraw(True)
    for _ in range(frames_per_sec * secs_of_msg):
        win.flip()
        check_exit()
    ophthalmic_info.setAutoDraw(False)
    win.flip()

    for frame_counter in range(frames_per_sec * secs_of_blinks):
        if frame_counter % frames_per_sec == 0 and send_triggers:
            trigger_no, triggers_list = prepare_trigger(trigger_type=TriggerTypes.BLINK, trigger_no=trigger_no,
                                                        triggers_list=triggers_list)
            send_trigger(port=port, trigger_no=trigger_no)
        win.flip()
        check_exit()

    corners_info.setAutoDraw(True)
    for _ in range(frames_per_sec * secs_of_msg):
        win.flip()
        check_exit()
    corners_info.setAutoDraw(False)

    [item.setAutoDraw(True) for item in crosses]
    for frame_counter in range(frames_per_sec * secs_of_saccades):
        if frame_counter % frames_per_sec == 0 and send_triggers:
            trigger_no, triggers_list = prepare_trigger(trigger_type=TriggerTypes.BLINK, trigger_no=trigger_no,
                                                        triggers_list=triggers_list)
            send_trigger(port=port, trigger_no=trigger_no)
        win.flip()
        check_exit()
    [item.setAutoDraw(False) for item in crosses]
    win.flip()

    logging.info('Ophthalmic procedure finished correctly!')

    return trigger_no, triggers_list
