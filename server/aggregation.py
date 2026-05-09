
import copy


def fedavg(client_updates):

    avg_weights = copy.deepcopy(client_updates[0])

    for key in avg_weights.keys():

        for i in range(1, len(client_updates)):

            avg_weights[key] += client_updates[i][key]

        avg_weights[key] = avg_weights[key] / len(client_updates)

    return avg_weights
