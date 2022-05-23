from psychopy import event, logging
from classes.save_data import save_beh, save_triggers


def check_exit(key="escape", part_id="", beh=None, triggers_list=None, results_dir=""):
    stop = event.getKeys(keyList=[key])
    if len(stop) > 0:
        if beh is not None and triggers_list is not None and results_dir != "":
            save_beh(beh, part_id, results_dir)
            save_triggers(triggers_list, part_id, results_dir)
        else:
            logging.critical("No data to save")

        logging.critical("Experiment finished by user! {} pressed.".format(key))
        exit(1)
