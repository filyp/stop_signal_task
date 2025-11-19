import time


class TriggerTypes(object):
    BLINK = "BLINK"
    GO = "GO"
    ST = "ST"
    RE = "RE"


# def create_eeg_port():
#     try:
#         import parallel

#         port = parallel.Parallel()
#         port.setData(0x00)
#         return port
#     except:
#         raise Exception("Can't connect to EEG")

def create_eeg_port():
    try:
        import serial

        port = serial.Serial("/dev/ttyUSB0", baudrate=115200)
        port.write(0x00)
        return port
    except:
        raise Exception("Can't connect to EEG")


def simple_send_trigger(port_eeg, trigger_no):
    port_eeg.write(trigger_no.to_bytes(1, 'big'))
    time.sleep(0.005)
    port_eeg.write(0x00)
    time.sleep(0.005)


def create_nirs_dev():
    try:
        import pyxid

        devices = pyxid.get_xid_devices()
        dev = devices[0]
        return dev
    except:
        raise Exception("Can't connect to NIRS")


def prepare_trigger_name(trial, correct_answer, stop_show_start=None):
    name = "*{}*{}".format(trial["arrow"]["TYPE"], trial["arrow"]["NAME"])
    if trial["stop"] is not None:
        name += "*{}*".format(
            trial["stop"]["STOP_TYPE"],
        )
        name += str(stop_show_start)
    else:
        name += "*-*-"
    name += "*{}".format(correct_answer)
    # for response
    name += "*-"
    return name


def prepare_trigger(trigger_no, triggers_list, trigger_type, trigger_name=None):
    trigger_no += 1
    if trigger_no == 9:
        trigger_no = 1
    if trigger_name is not None:
        trigger_type = trigger_type + trigger_name
    triggers_list.append((str(trigger_no), trigger_type))
    return trigger_no, triggers_list


def send_trigger(
    trigger_no, port_eeg=None, port_nirs=None, send_eeg_triggers=False, send_nirs_triggers=False
):
    if send_eeg_triggers:
        try:
            simple_send_trigger(port_eeg, trigger_no)
        except:
            pass
    if send_nirs_triggers:
        try:
            port_nirs.activate_line(trigger_no)
        except:
            pass


def amend_trial_triggers_in_reaction_before_stop(triggers_list):
    for i in range(1, 10):
        # go back through triggers list and swap *0* for *1*
        trigger_no, trigger_body = triggers_list[-i]
        trigger_body = trigger_body.replace("*0*", "*1*")
        triggers_list[-i] = (trigger_no, trigger_body)

        # if we hit "GO" trigger, break
        if "GO*" in trigger_body:
            break
