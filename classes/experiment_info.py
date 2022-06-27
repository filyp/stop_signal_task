import datetime
from psychopy import gui


def experiment_info(observer):
    """
    okienko dialogowe na podczas uruchomienia procedury
    :param observer: observer_id
    :return: part_id, observer_id, date
    """

    my_dlg = gui.Dlg(title="SST")
    my_dlg.addText("Informacje:")
    my_dlg.addField("ID:")

    my_dlg.show()
    if not my_dlg.OK:
        exit(1)

    #          id
    return my_dlg.data[0]


def eeg_info():
    """
    Dialog info shows at the beginning of the experiment.
    """

    my_dlg = gui.Dlg(title="SST")
    my_dlg.addText("\n\tZanim zaczniesz zadanie, uruchom ActiView i rozpocznij zapis.")
    my_dlg.addText("")

    my_dlg.show()
    if not my_dlg.OK:
        exit(1)
