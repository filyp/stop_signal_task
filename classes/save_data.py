import os
import csv


def save_triggers(data, name):
    rows = [row[0] + ":" + row[1] for row in data]
    path = os.path.join("results", "triggers_maps", "triggerMap_{}.txt".format(name))
    with open(path, "wb") as map_file:
        text = "\n".join(rows)
        # this must be done in such an awkward way, to prevent OS specific EOL
        map_file.write(bytes(text, "UTF-8"))


def save_beh(data, name):
    print(data)
    with open(
        os.path.join("results", "behavioral_data", "beh_{}.csv".format(name)), "w"
    ) as csvfile:
        fieldnames = [
            "Nr",
            "GO_type",
            "GO_name",
            "RE_key",
            "RE_true",
            "RE_time",
            "ST_type",
            "ST_name",
            "ST_wait_time",
            "STOP_TYPE",
        ]
        writer = csv.DictWriter(csvfile, fieldnames=fieldnames)
        writer.writeheader()
        for row in data:
            writer.writerow(row)
