import os
import csv


def save_triggers(data, name):
    with open(os.path.join('results', 'triggers_maps', 'triggerMap_{}.txt'.format(name)), 'w') as mapFile:
        mapFile.writelines(data)


def save_beh(data, name):
    with open(os.path.join('results', 'behavioral_data', 'beh_{}.txt'.format(name)), 'w') as csvfile:
        fieldnames = ['Nr', 'GO_name', 'RE_name', 'RE_time', 'ST_name', 'ST_wait_time']
        writer = csv.DictWriter(csvfile, fieldnames=fieldnames)
        writer.writeheader()
        for row in data:
            writer.writerow(row)
