import os
import csv


def save_triggers(data, name):
    data = [row[0]+':'+row[1]+'\n' for row in data]
    with open(os.path.join('results', 'triggers_maps', 'triggerMap_{}.txt'.format(name)), 'w') as mapFile:
        for row in data:
            mapFile.writelines(row)


def save_beh(data, name):
    with open(os.path.join('results', 'behavioral_data', 'beh_{}.txt'.format(name)), 'w') as csvfile:
        fieldnames = ['Nr', 'GO_name', 'RE_name', 'RE_time', 'ST_name', 'ST_wait_time']
        writer = csv.DictWriter(csvfile, fieldnames=fieldnames)
        writer.writeheader()
        for row in data:
            writer.writerow(row)
