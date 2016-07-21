import time


class TriggerTypes(object):
    BLINK = 'BLINK'
    GO = 'GO'
    ST = 'ST'
    RE = 'RE'


def create_eeg_port():
    try:
        import parallel
        port = parallel.Parallel()
        port.setData(0x00)
        return port
    except:
        raise Exception("Can't connect to EEG")


def create_nirs_dev():
    try:
        import pyxid
        devices = pyxid.get_xid_devices()
        dev = devices[0]
        return dev
    except:
        raise Exception("Can't connect to NIRS")


def prepare_trigger(trigger_type, trigger_no, triggers_list):
    trigger_no += 1
    if trigger_no == 9:
        trigger_no = 1
    triggers_list.append((str(trigger_no), trigger_type))
    return trigger_no, triggers_list


def send_trigger(port, trigger_no):
    try:
        port.setData(trigger_no)
        time.sleep(0.01)
        port.setData(0x00)
    except:
        try:
            port.activate_line(trigger_no)
        except:
            raise Exception("Can't send trigger")
