import time


class TriggerTypes(object):
    BLINK = 'BLINK'
    GO = 'GO'
    ST = 'ST'
    RE = 'RE'


def prepare_trigger(trigger_type, trigger_no, triggers_list):
    trigger_no += 1
    if trigger_no == 61:
        trigger_no = 1
    triggers_list.append((str(trigger_no), trigger_type))
    return trigger_no, triggers_list


def send_trigger(port, trigger_no):
    port.setData(trigger_no)
    time.sleep(0.01)
    port.setData(0x00)
