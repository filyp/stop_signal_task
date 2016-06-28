import random


def prepare_arrows(number_of_arrows_types, number_of_trials):
    arrows_table = range(number_of_arrows_types) * (number_of_trials / number_of_arrows_types)

    missing_trials = number_of_trials % number_of_arrows_types
    rest_trials = range(number_of_arrows_types)
    random.shuffle(rest_trials)

    arrows_table += rest_trials[:missing_trials]
    random.shuffle(arrows_table)

    return arrows_table


def prepare_stops(number_of_stop_types, number_of_trials, percent_of_trials_with_stop=25):
    number_of_trials_with_stop = number_of_trials * percent_of_trials_with_stop / 100
    stop_table = range(number_of_stop_types) * (number_of_trials_with_stop / number_of_stop_types)

    missing_trials = number_of_trials_with_stop % number_of_stop_types
    rest_trials = range(number_of_stop_types)
    random.shuffle(rest_trials)

    stop_table += rest_trials[:missing_trials]

    # -1 w stop_table oznacza trial bez stopa
    trials_without_stop = [-1] * (number_of_trials - 2 * len(stop_table))
    stop_table += trials_without_stop
    random.shuffle(stop_table)

    # zapewnienie, ze nie bedzie dwoch stopow pod rzad
    new_stop_table = []
    for trial in stop_table:
        new_stop_table.append(trial)
        if trial >= 0:
            new_stop_table.append(-1)

    return new_stop_table


def blocks_creator(arrows_table, stop_table, num):
    assert len(stop_table) == len(arrows_table), "len(stop_table) != len(arrows_table)"
    zipped = [{'arrow': arrow, 'stop': stop} for arrow, stop in zip(arrows_table, stop_table)]
    blocks = [zipped[i:i + len(zipped) / num] for i in range(0, len(zipped), len(zipped) / num)]
    return blocks


def prepare_trials(number_of_blocks, number_of_experiment_trials, number_of_training_trials,
                   number_of_stop_types, percent_of_trials_with_stop, number_of_arrows):
    assert percent_of_trials_with_stop <= 50, "procent stopow nie moze byc wiekszy od 50"

    # prepare training
    training_arrows_table = prepare_arrows(number_of_arrows_types=number_of_arrows,
                                           number_of_trials=number_of_training_trials)

    training_stop_table = prepare_stops(number_of_stop_types=number_of_stop_types,
                                        number_of_trials=number_of_training_trials,
                                        percent_of_trials_with_stop=percent_of_trials_with_stop)

    training_block = blocks_creator(arrows_table=training_arrows_table, stop_table=training_stop_table, num=1)

    # prepare experiment
    experiment_arrows_table = prepare_arrows(number_of_arrows_types=number_of_arrows,
                                             number_of_trials=number_of_experiment_trials)

    experiment_stop_table = prepare_stops(number_of_stop_types=number_of_stop_types,
                                          number_of_trials=number_of_experiment_trials,
                                          percent_of_trials_with_stop=percent_of_trials_with_stop)

    experiment_block = blocks_creator(arrows_table=experiment_arrows_table,
                                      stop_table=experiment_stop_table,
                                      num=number_of_blocks)

    print training_block
    print experiment_block


prepare_trials(number_of_blocks=2, number_of_experiment_trials=10, number_of_training_trials=20,
               number_of_stop_types=2, percent_of_trials_with_stop=50, number_of_arrows=2)
