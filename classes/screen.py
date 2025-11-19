from collections import OrderedDict

from psychopy import logging, visual, event
from screeninfo import get_monitors


def get_screen_res(screen_number=0):
    """
    Funcion that check current screen resolution. Raise OSError if can't recognise OS!
    * :return: (width, height) tuple with screen resolution.
    """
    monitor = get_monitors()[screen_number]
    logging.info("Screen res set as: {}x{}".format(monitor.width, monitor.height))

    return OrderedDict(width=monitor.width, height=monitor.height)


def get_frame_rate(win, legal_frame_rates=(144, 60, 30)):
    frame_rate = int(round(win.getActualFrameRate(nIdentical=30, nMaxFrames=200)))
    logging.info("Detected framerate: {} frames per sec.".format(frame_rate))
    assert frame_rate in legal_frame_rates, "Illegal frame rate."
    return frame_rate


def create_win(screen_color, screen_number):
    """
    zwraca ekran na ktorym bedzie wszystko wyswietlane
    wylacza myszke
    :param screen_color: kolor tla
    :return: zwraca ekran na ktorym bedzie wszystko wyswietlane
    """
    screen_res = get_screen_res(screen_number)
    screen_res_list = list(screen_res.values())
    win = visual.Window(
        screen_res_list,
        fullscr=True,
        units="height",
        screen=screen_number,
        color=screen_color,
    )
    event.Mouse(visible=False, newPos=None, win=win)
    win.flip()
    frames_per_sec = get_frame_rate(win=win)
    return win, screen_res, frames_per_sec
