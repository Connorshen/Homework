# 目标函数:maxf(x)=x1^2+x2^2+x3^2
# 约束条件:x1=[0,7],x2=[0,7],x3=[0,7]
import numpy as np


# 个体
class Individual:
    fitness = 0

    def __init__(self):
        self.chromosome = Chromosome([np.random.randint(0, 8) for _ in range(3)])


# 染色体
class Chromosome:
    value = ""

    def __init__(self, xs):
        for x in xs:
            self.value += str(bin(x)).replace("0b", "").zfill(3)

    def decode(self):
        return [int(self.value[0:3], 2), int(self.value[3:6], 2), int(self.value[6:9], 2)]


class GA:
    def calculate_fitness(self, pop):
        for individual in pop:
            individual.fitness = self.fitness(individual.chromosome.decode())

    def fitness(self, xs):
        return xs[0] ** 2 + xs[1] ** 2 + xs[2] ** 2

    def fitness_sum(self, pop):
        sum = 0
        for individual in pop:
            sum += individual.fitness
        return sum

    def fitness_avg(self, pop):
        return self.fitness_sum(pop) / len(pop)

    def selection(self, pop):
        fitness_sum = self.fitness_sum(pop)
        p_select = []
        b_select = 0
        for individual in pop:
            c_select = individual.fitness / fitness_sum
            p_select.append([b_select, b_select + c_select])
            b_select = b_select + c_select
        selected_pop = []
        for _ in range(len(pop)):
            e = np.random.rand()
            selected_pop.append(self.in_range(pop, e, p_select))
        return selected_pop

    def in_range(self, pop, p, p_select):
        for i in range(len(p_select)):
            if p_select[i][0] <= p <= p_select[i][1]:
                return pop[i]

    def init_pop(self, pop):
        self.calculate_fitness(pop)

    def evolution(self, pop, episode):
        for _ in range(episode):
            pop = self.selection(pop)
            self.calculate_fitness(pop)
            print(self.fitness_avg(pop))


if __name__ == '__main__':
    POP_SIZE = 10
    EPISODE = 100
    ga = GA()
    pop = [Individual() for _ in range(POP_SIZE)]
    ga.init_pop(pop)
    ga.evolution(pop, EPISODE)
