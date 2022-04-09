import copy
from itertools import permutations
from random import sample, randint, choice


class DTSP:
    def get_timed_weights(self, time) -> list[int]:
        weights = [weight_func(time) for weight_func in self.weights]
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
        paths: list[list[int]] = list(map(list, permutations(self.nodes)))
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

    def apply_crossover(self, a: list[int], b: list[int]):
        n = len(a)
        gen_a, gen_b = a[1:n-1], b[1:n-1]
        n = len(gen_a)
        start = randint(0, n-1)
        end = randint(start, n-1)
        c = [-1] * n
        c[start:end+1] = gen_a[start:end+1]
        if -1 in c:
            new_b = [-1] * n
            for i in range(n):
                new_b[i] = gen_b[(i+end)%n]
            to_add = []
            a_slice = gen_a[start:end+1]
            for i in range(n):
                if new_b[i] not in a_slice:
                    to_add.append(new_b[i])
            for i in range(len(to_add)):
                c[(i+end+1)%n] = to_add[i]
        return [self.start_node, *c, self.start_node]

    def simulate(self, steps: int):
        cycles = self.gen_random_cycles()
        for _ in range(steps):
            sorted_cycles = sorted(cycles, key=self.count_cycle_time)
            # print(sorted_cycles, list(map(self.count_cycle_time, sorted_cycles)))
            sorted_cycles = sorted_cycles[:len(cycles) // 2]
            cycles = copy.deepcopy(sorted_cycles)
            for cycle in sorted_cycles:
                p2 = copy.copy(choice(sorted_cycles))
                c = self.apply_crossover(copy.copy(cycle), p2)
                if randint(0, 100) < self.mutation_prob:
                    c = copy.copy(self.apply_mutation(c))
                cycles.append(c)
        return cycles

    def __init__(self, nodes, node_times, edges, weights, start_time, start_node, mutation_prob):
        self.mutation_prob = mutation_prob
        self.start_time = start_time
        self.weights = weights
        self.edges = edges
        self.node_times = node_times
        self.nodes = nodes
        self.time_now = start_time
        self.start_node = start_node
