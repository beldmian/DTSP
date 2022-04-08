from DTSP import DTSP

if __name__ == '__main__':
    nodes: list[int] = [0, 1, 2, 3]
    node_times: list[int] = [1, 2, 1, 1]
    edges: list[tuple[int, int]] = [(0, 1), (0, 2), (0, 3), (1, 2), (1, 3), (2, 3)]
    weights: dict[int, list[int]] = {
        0: [1, 1, 1, 1, 1, 1],
        2: [3, 3, 3, 2, 3, 2],
        3: [1, 1, 2, 1, 2, 1]
    }
    start_time: int = 0
    dtsp = DTSP(nodes, node_times, edges, weights, start_time)
    cycle = dtsp.simulate(100)[0]
    print(cycle, dtsp.count_cycle_time(cycle))
