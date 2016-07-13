"""
import parallel

PORT = parallel.Parallel()
"""
PORT = None
TRIGGER_NO = 0
TRIGGERS_LIST = list()


class TriggerTypes(object):
    BLINK = 'BLINK'
    RELATION_SHOWED = 'RELATION_SHOWED'
    STOP_SHOWED = 'STOP_SHOWED'
    PARTICIPANT_RESPOND = 'PARTICIPANT_RESPOND'


def prepare_trigger(trigger_type):
    global TRIGGER_NO
    TRIGGER_NO += 1
    if TRIGGER_NO == 61:
        TRIGGER_NO = 1
    TRIGGERS_LIST.append((str(TRIGGER_NO), trigger_type))
    return TRIGGER_NO
