import copy
from itertools import permutations
from random import sample, randint, choice, shuffle
from math import factorial, exp


def perm_given_index(alist, apermindex):
    alist = alist[:]
    for i in range(len(alist) - 1):
        apermindex, j = divmod(apermindex, len(alist) - i)
        alist[i], alist[i + j] = alist[i + j], alist[i]
    return alist


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
            node = cycle[j]
            prev_node = cycle[j - 1]
            w = self.get_timed_weights(end_time)
            for i in range(len(self.edges)):
                edge = self.edges[i]
                if edge == (prev_node, node) or edge == (node, prev_node):
                    end_time += w[i]
        return end_time - self.start_time

    def gen_random_cycles(self, count: int):
        paths = []
        if len(self.nodes) < 5:
            paths = list(map(list, permutations(self.nodes)))
        else:
            max_ind = factorial(len(self.nodes) - 1)
            perm_nodes = copy.copy(self.nodes)
            perm_nodes.remove(self.start_node)
            for _ in range(count):
                ind = randint(0, max_ind)
                paths.append([self.start_node] + perm_given_index(perm_nodes, ind))
        cycles = []
        for path in paths:
            if path[0] != self.start_node:
                continue
            cycle = list(path)
            cycle.append(path[0])
            cycles.append(cycle)

        return sample(cycles, min(100, len(cycles)))

    def apply_mutation(self, cycle: list[int]):
        slice_size = randint(2, 6)
        end_slice = randint(slice_size + 1, len(self.nodes) - 1)
        start_slice = end_slice - slice_size
        cycle_part = copy.copy(cycle[start_slice:end_slice])
        shuffle(cycle_part)
        cycle[start_slice:end_slice] = cycle_part
        # permutation_list = permutations(cycle_part)
        # min_perm = []
        # min_perm_length = float("inf")
        # for permutation in permutation_list:
        #     length = self.count_cycle_time(list(permutation))
        #     if length < min_perm_length:
        #         min_perm = permutation
        #         min_perm_length = length
        # cycle[start_slice:end_slice] = min_perm
        return cycle

    def apply_crossover(self, a: list[int], b: list[int]):
        a, b = a[:], b[:]
        n = len(a)
        gen_a, gen_b = a[1:n - 1], b[1:n - 1]
        n = len(gen_a)
        start = randint(0, n - 1)
        end = randint(start, n - 1)
        c = [-1] * n
        c[start:end + 1] = gen_a[start:end + 1]
        if -1 in c:
            new_b = [-1] * n
            for i in range(n):
                new_b[i] = gen_b[(i + end) % n]
            to_add = []
            a_slice = gen_a[start:end + 1]
            for i in range(n):
                if new_b[i] not in a_slice:
                    to_add.append(new_b[i])
            for i in range(len(to_add)):
                c[(i + end + 1) % n] = to_add[i]
        return [self.start_node, *c, self.start_node]

    def apply_crossover_new(self, a: list[int], b: list[int]):
        n = len(a)
        a, b = a[1:n - 1], b[1:n - 1]
        n = len(a)
        slice_start = randint(0, n - 2)
        slice_end = randint(slice_start + 2, n)
        slice_a = a[slice_start:slice_end]
        indexes = {}
        for x in slice_a:
            indexes[x] = b.index(x)
        new_slice = list(map(lambda y: y[0], sorted(list(indexes.items()), key=lambda y: y[1])))
        a[slice_start:slice_end] = new_slice
        return [self.start_node, *a, self.start_node]

    def simulate(self, steps: int, cycles):
        for _ in range(steps):
            sorted_cycles = sorted(cycles, key=self.count_cycle_time)
            print(sorted_cycles, list(map(self.count_cycle_time, sorted_cycles)))
            sorted_cycles = sorted_cycles[:len(cycles) // 2]
            cycles = copy.deepcopy(sorted_cycles)
            for i in range(len(sorted_cycles)):
                p2 = copy.copy(choice(sorted_cycles))
                c = self.apply_crossover(copy.copy(sorted_cycles[i]), p2)
                # c = self.apply_crossover_new(copy.copy(sorted_cycles[i]), p2)
                cycles.append(c)
            for i in range(len(cycles)):
                if i == 0:
                    continue
                if randint(0, 100) < self.mutation_prob * 100:
                    cycles[i] = copy.copy(self.apply_mutation(copy.copy(cycles[i])))
        return cycles

    def two_factor_simulate(self, steps: int, count: int):
        cycles = []
        print("### first ###")
        for i in range(count):
            print("#", i)
            sim_cycles = self.gen_random_cycles(5)
            local_cycles = self.simulate(10, sim_cycles)
            cycles.append(local_cycles[0])
        print("### second ###")
        return self.simulate(steps, cycles)

    def decrease_temp(self, initial_t, i):
        return initial_t * 0.1 / i

    def new_cycle(self, prev_cycle: list[int]):
        prev_cycle = prev_cycle[:]
        i = randint(1, len(prev_cycle) - 1)
        j = randint(1, len(prev_cycle) - 1)
        if i > j:
            cycle_slice = prev_cycle[j:i]
            prev_cycle[j:i] = cycle_slice[::-1]
        else:
            cycle_slice = prev_cycle[i:j]
        prev_cycle[i:j] = cycle_slice[::-1]
        return prev_cycle

    def simulated_annealing(self, initial_t: float, end_t: float):
        i = 1
        s = self.gen_random_cycles(1)[0]
        t = self.decrease_temp(initial_t, i)
        while t > 0:
            new_s = self.new_cycle(copy.copy(s))
            delta_e = self.count_cycle_time(new_s) - self.count_cycle_time(s)
            if delta_e < 0:
                s = new_s
            if delta_e > 0:
                if randint(1, 101) / 100 < exp(-delta_e / t):
                    s = new_s
            i += 1
            t = self.decrease_temp(initial_t, i)
            print(s, self.count_cycle_time(s))
        return s

    def __init__(self, nodes, node_times, edges, weights, start_time, start_node, mutation_prob):
        self.mutation_prob = mutation_prob
        self.start_time = start_time
        self.weights = weights
        self.edges = edges
        self.node_times = node_times
        self.nodes = nodes
        self.time_now = start_time
        self.start_node = start_node
