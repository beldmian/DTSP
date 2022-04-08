import copy
from itertools import permutations
from random import sample, randint

class DTSP:
    nodes: list[int]
    node_times: list[int]
    edges: list[tuple[int, int]]
    weights: dict[int, list[int]]
    start_time: int
    time_now: int

    def get_timed_weights(self, time) -> list[int]:
        time_interval = 0
        intervals = list(self.weights.keys())
        for i in range(len(intervals)):
            if i == 0:
                continue
            if intervals[i - 1] <= time < intervals[i]:
                time_interval = intervals[i-1]
                break
            if i == len(intervals):
                time_interval = intervals[i]
                break
        weights = self.weights[time_interval]
        return weights

    def count_cycle_time(self, cycle: list[int]) -> int:
        end_time = self.start_time
        for j in range(len(cycle)):
            end_time += self.node_times[cycle[j]]
            if j == 0:
                continue
            w = self.get_timed_weights(end_time)
            for i in range(len(self.edges)):
                edge = self.edges[i]
                if edge == (j-1, j) or edge == (j, j-1):
                    end_time += w[i]
        return end_time-self.start_time

    def gen_random_cycles(self):
        paths = list(permutations(self.nodes))
        cycles = []
        for path in paths:
            if path[0] != self.start_node:
                continue
            cycle = list(path)
            cycle.append(path[0])
            cycles.append(cycle)

        return sample(cycles, min(100, len(cycles)))

    @staticmethod
    def apply_mutation(cycle: list[int]):
        a, b = randint(1, len(cycle)-2), randint(1, len(cycle)-2)
        cycle[a], cycle[b] = cycle[b], cycle[a]
        return cycle

    def simulate(self, steps: int):
        cycles = self.gen_random_cycles()
        for _ in range(steps):
            sorted_cycles = sorted(cycles, key=self.count_cycle_time)
            # print(sorted_cycles, list(map(self.count_cycle_time, sorted_cycles)))
            sorted_cycles = sorted_cycles[:len(cycles) // 2]
            cycles = copy.deepcopy(sorted_cycles)
            for cycle in sorted_cycles:
                mutated_cycle = copy.copy(self.apply_mutation(cycle))
                cycles.append(mutated_cycle)
        return cycles

    def __init__(self, nodes, node_times, edges, weights, start_time, start_node):
        self.start_time = start_time
        self.weights = weights
        self.edges = edges
        self.node_times = node_times
        self.nodes = nodes
        self.time_now = start_time
        self.start_node = start_node

