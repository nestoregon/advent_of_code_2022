"""
This is going to be a hard problem.
The goal of the problem is an optimization problem.

The more time it goes by, the less optimal solutions will become.
It takes:
    - 1 minute to travel
    - 1 minute to open a valve
    - Total amount = time * valve value
"""

import networkx as nx
import matplotlib.pyplot as plt

from typing import List


def read_input_as_lines(input_path: str) -> List[str]:
    with open(input_path) as f:
        lines = f.readlines()
    lines = [line.strip() for line in lines]
    return lines


def transform_input_to_graph_nx(input, minutes_to_travel=1):
    graph = nx.Graph()
    for line in input:
        text_chunks = line.replace(',', '').split()
        node_name = text_chunks[1]
        edges = text_chunks[9:]
        graph.add_node(
            node_name,
            valve_value=int(text_chunks[4][5:-1]),
            travel=minutes_to_travel,
        )
        for edge in edges:
            graph.add_edge(node_name, edge)
    return graph


def find_next_room_with_most_gain(
    current_room, valve_values, shortest_paths, minutes_available, rooms_visited
):
    room_to_gain = {}
    rooms_to_cover = set(valve_values.keys()) - rooms_visited

    for room in rooms_to_cover:
        time_consumed = shortest_paths[current_room][room]
        remaining_time = minutes_available - time_consumed - 1

        if 0 > remaining_time:  # can we actually do it?
            continue

        gain = remaining_time * valve_values[room]
        room_to_gain[room] = (gain, remaining_time)

    if len(room_to_gain) == 0:
        return 0, 0, 0

    room_to_gain = dict(sorted(room_to_gain.items(), key=lambda item: item[1], reverse=True))
    best_choice = next(iter(room_to_gain))
    best_gain, time = room_to_gain[best_choice]

    return best_choice, best_gain, time


def get_greedy_method(graph, minutes_avaliable: int) -> int:
    valve_values = nx.get_node_attributes(graph, "valve_value")
    valve_values = {k: v
                    for k, v in valve_values.items() if v > 0}
    valve_values = dict(sorted(valve_values.items(), key=lambda item: item[1], reverse=True))
    shortest_paths = dict(nx.all_pairs_shortest_path_length(graph))

    score = 0
    current_room = 'AA'
    rooms_visited = set([current_room])

    print(f'GREEDY: Starting at {current_room}, score {score}')
    while minutes_avaliable > 0:
        next_room, gain, minutes_avaliable = find_next_room_with_most_gain(
            current_room,
            valve_values,
            shortest_paths,
            minutes_avaliable,
            rooms_visited,
        )
        if next_room == 0:  # there's nothing else to do.
            break
        score += gain
        print(
            f'- From {current_room} is best to go to {next_room}, with a gain '
            f'of {gain} and {minutes_avaliable} minutes available & score = {score}'
        )
        rooms_visited.add(next_room)
        current_room = next_room  # update

    print(f'Greedy algorithm score = {score}')
    return score


def save_graph_to_image(graph, image_name: str = 'graph.png'):
    nx.draw(graph, with_labels=True, font_weight='bold')
    plt.show()
    # name = nx.get_node_attributes(graph, 'pos')
    # nx.draw(graph, pos=name)
    # labels = nx.get_edge_attributes(graph, 'valve_value')
    # nx.draw_networkx_edge_labels(graph, name, edge_labels=labels)
    plt.savefig(image_name)


def main():
    input = read_input_as_lines('easy_input.txt')
    graph = transform_input_to_graph_nx(input)
    get_greedy_method(graph, minutes_avaliable=30)
    save_graph_to_image(graph)


if __name__ == '__main__':
    main()
