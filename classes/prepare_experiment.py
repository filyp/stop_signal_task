import random


def prepare_arrows(arrows, number_of_trials):
    number_of_arrows_types = len(arrows)
    arrows_table = list(range(number_of_arrows_types)) * int(
        number_of_trials / number_of_arrows_types
    )

    missing_trials = number_of_trials % number_of_arrows_types
    rest_trials = list(range(number_of_arrows_types))
    random.shuffle(rest_trials)

    arrows_table += rest_trials[:missing_trials]
    # random.shuffle(arrows_table)

    arrows_table = [arrows[x] for x in arrows_table]

    return arrows_table


def prepare_stops(stops, number_of_trials, arrows_table, percent_of_trials_with_stop=25):
    number_of_stop_types = len(stops)
    number_of_trials_with_stop = int(round(number_of_trials * percent_of_trials_with_stop / 100.0))
    stop_table = list(range(number_of_stop_types)) * int(
        number_of_trials_with_stop / number_of_stop_types
    )
    missing_trials = number_of_trials_with_stop % number_of_stop_types
    rest_trials = list(range(number_of_stop_types))
    stop_table += rest_trials[:missing_trials]
    stop_table = sorted(stop_table)
    trials_with_stop = [
        {"arrow": arrow, "stop": stops[stop]}
        for arrow, stop in zip(arrows_table[: len(stop_table)], stop_table)
    ]
    random.shuffle(trials_with_stop)
    arrows_table = arrows_table[len(stop_table) :]
    random.shuffle(arrows_table)
    # removing trials with stops with are one by one
    new_stop_table = []
    for trial in trials_with_stop:
        new_stop_table.append(trial)
        new_stop_table.append({"arrow": arrows_table[0], "stop": None})
        arrows_table = arrows_table[1:]
    return new_stop_table, arrows_table


def blocks_creator(trials, num, breaks):
    blocks = [
        trials[i : i + int(len(trials) / num)]
        for i in range(0, len(trials), int(len(trials) / num))
    ]
    # add instructions
    blocks = [{"trials": block, "text_after_block": text} for block, text in zip(blocks, breaks)]
    return blocks


def random_insert(lst, item):
    lst.insert(random.randrange(len(lst) + 1), item)


def prepare_trials(
    number_of_blocks,
    number_of_experiment_trials,
    stops,
    percent_of_trials_with_stop,
    arrows,
    messages,
):
    assert percent_of_trials_with_stop <= 50, "procent stopow nie moze byc wiekszy od 50"

    arrows_table = prepare_arrows(arrows=arrows, number_of_trials=number_of_experiment_trials)

    trials, rest_arrows = prepare_stops(
        stops=stops,
        arrows_table=arrows_table,
        number_of_trials=number_of_experiment_trials,
        percent_of_trials_with_stop=percent_of_trials_with_stop,
    )

    for elem in rest_arrows:
        random_insert(trials, {"arrow": elem, "stop": None})

    experiment_block = blocks_creator(trials=trials, num=number_of_blocks, breaks=messages)

    return experiment_block


def create_stops_times_dict(stops, start_wait_to_stop):
    stops_times = dict()
    for stop in stops:
        stops_times[stop["WORD_EMO"]] = start_wait_to_stop
    return stops_times


def randomize_buttons(old_dict):
    buttons = list(set(old_dict.values()))
    buttons_rand = list(set(old_dict.values()))
    random.shuffle(buttons_rand)
    new_dict = dict()
    for key in old_dict:
        idx = buttons.index(old_dict[key])
        new_dict[key] = buttons_rand[idx]

    return new_dict
