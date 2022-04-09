from DTSP import DTSP

if __name__ == '__main__':
    nodes: list[int] = [0, 1, 2, 3]
    node_times: list[int] = [1, 2, 1, 1]
    edges: list[tuple[int, int]] = [(0, 1), (0, 2), (0, 3), (1, 2), (1, 3), (2, 3)]
    weights: list = [
        lambda t: 3 if 3 > t >= 2 else 1,
        lambda t: 3 if 3 > t >= 2 else 1,
        lambda t: 1 if 2 > t >= 0 else 3 if 3 > t >= 2 else 2,
        lambda t: 2 if 3 > t >= 2 else 1,
        lambda t: 1 if 2 > t >= 0 else 3 if 3 > t >= 2 else 2,
        lambda t: 2 if 3 > t >= 2 else 1,
    ]
    start_time: int = 0
    start_node: int = 0
    mutation_prob: float = 0.5

    dtsp = DTSP(nodes, node_times, edges, weights, start_time, start_node, mutation_prob)
    cycle = dtsp.simulate(100)[0]
    print(cycle, dtsp.count_cycle_time(cycle))
