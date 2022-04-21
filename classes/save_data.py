import os
import csv


def save_triggers(data, name, results_dir):
    trigger_directory = os.path.join(results_dir, "triggers_maps")
    os.makedirs(trigger_directory, exist_ok=True)
    rows = [row[0] + ":" + row[1] for row in data]
    path = os.path.join(trigger_directory, "triggerMap_{}.txt".format(name))
    with open(path, "wb") as map_file:
        text = "\n".join(rows)
        # this must be done in such an awkward way, to prevent OS specific EOL
        map_file.write(bytes(text, "UTF-8"))


def save_beh(data, name, results_dir):
    print(data)
    behavioral_directory = os.path.join(results_dir, "behavioral_data")
    os.makedirs(behavioral_directory, exist_ok=True)
    with open(os.path.join(behavioral_directory, "beh_{}.csv".format(name)), "w") as csvfile:
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
