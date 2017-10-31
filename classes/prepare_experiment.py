import random
import os


def prepare_arrows(arrows, number_of_trials):
    number_of_arrows_types = len(arrows)
    arrows_table = range(number_of_arrows_types) * (number_of_trials / number_of_arrows_types)

    missing_trials = number_of_trials % number_of_arrows_types
    rest_trials = range(number_of_arrows_types)
    random.shuffle(rest_trials)

    arrows_table += rest_trials[:missing_trials]
    random.shuffle(arrows_table)

    arrows_table = [arrows[x] for x in arrows_table]

    return arrows_table


def prepare_stops(stops, number_of_trials, percent_of_trials_with_stop=25):
    number_of_stop_types = len(stops)
    number_of_trials_with_stop = number_of_trials * percent_of_trials_with_stop / 100
    stop_table = range(number_of_stop_types) * (number_of_trials_with_stop / number_of_stop_types)

    missing_trials = number_of_trials_with_stop % number_of_stop_types
    rest_trials = range(number_of_stop_types)
    random.shuffle(rest_trials)

    stop_table += rest_trials[:missing_trials]

    # create trials without stops
    trials_without_stop = [None] * (number_of_trials - 2 * len(stop_table))
    stop_table += trials_without_stop
    random.shuffle(stop_table)

    # removing trials with stops with are one by one
    new_stop_table = []
    for trial in stop_table:
        new_stop_table.append(trial)
        if trial >= 0:
            new_stop_table.append(None)

    new_stop_table = [stops[x] if x is not None else None for x in new_stop_table]

    return new_stop_table


def blocks_creator(arrows_table, stop_table, num, breaks):
    assert len(stop_table) == len(arrows_table), "len(stop_table) != len(arrows_table)"
    zipped = [{'arrow': arrow, 'stop': stop} for arrow, stop in zip(arrows_table, stop_table)]
    blocks = [zipped[i:i + len(zipped) / num] for i in range(0, len(zipped), len(zipped) / num)]
    # add instructions
    blocks = [{'trials': block, 'text_after_block': text} for block, text in zip(blocks, breaks)]
    return blocks


def prepare_trials(number_of_blocks, number_of_experiment_trials, stops, percent_of_trials_with_stop, arrows, messages):
    assert percent_of_trials_with_stop <= 50, "procent stopow nie moze byc wiekszy od 50"

    experiment_arrows_table = prepare_arrows(arrows=arrows,
                                             number_of_trials=number_of_experiment_trials)

    experiment_stop_table = prepare_stops(stops=stops,
                                          number_of_trials=number_of_experiment_trials,
                                          percent_of_trials_with_stop=percent_of_trials_with_stop)

    experiment_block = blocks_creator(arrows_table=experiment_arrows_table,
                                      stop_table=experiment_stop_table,
                                      num=number_of_blocks,
                                      breaks=messages)

    return experiment_block


def create_stops_times_dict(stops, start_wait_to_stop):
    stops_times = dict()
    for stop in stops:
        stops_times[stop[1].split('_')[0]] = start_wait_to_stop
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
