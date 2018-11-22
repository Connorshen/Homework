# 目标函数:maxf(x)=x1^2+x2^2+x3^2
# 约束条件:x1=[0,7],x2=[0,7],x3=[0,7]
import numpy as np


class Individual:
    fitness = 0

    def __init__(self):
        self.t = [np.random.randint(0, 8) for _ in range(3)]
        self.chromosome = Chromosome(self.t)


class Chromosome:
    value = ""

    def __init__(self, xs):
        for x in xs:
            self.value += str(bin(x)).replace("0b", "").zfill(3)

    def decode(self):
        return [int(self.value[0:3], 2), int(self.value[3:6], 2), int(self.value[6:9], 2)]


class GA:
    def calculate_fitness(self, individual):
        individual.fitness = self.fitness(individual.chromosome.decode())
        return individual.fitness

    def fitness(self, xs):
        return xs[0] ** 2 + xs[1] ** 2 + xs[2] ** 2


if __name__ == '__main__':
    pass
