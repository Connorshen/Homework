import numpy as np
import random
import matplotlib.pyplot as plt


# 目标函数:maxf(x)=x1^2+x2^2+x3^2
# 约束条件:x1=[0,7],x2=[0,7],x3=[0,7]

# TODO:添加约束函数，现在是通过染色体的个数来约束的
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

    def alternate(self, pop):
        pop_size = len(pop)
        index_all = [i for i in range(pop_size)]
        index_one = random.sample(index_all, int(pop_size / 2))
        index_two = [i for i in index_all if i not in index_one]
        for i in range(int(pop_size / 2)):
            chromosome_len = len(pop[i].chromosome.value)
            start = np.random.randint(0, chromosome_len)
            end = np.random.randint(0, chromosome_len)
            if start > end: start, end = end, start
            one = pop[index_one[i]].chromosome.value
            two = pop[index_two[i]].chromosome.value
            one_replace = one[start:end + 1]
            two_replace = two[start:end + 1]
            pop[index_one[i]].chromosome.value = one[0:start] + two_replace + one[end + 1:]
            pop[index_two[i]].chromosome.value = two[0:start] + one_replace + two[end + 1:]
        self.calculate_fitness(pop)
        return pop

    def variation(self, pop, variation):
        for individual in pop:
            if np.random.random() < variation:
                chromosome_len = len(individual.chromosome.value)
                var_index = np.random.randint(0, chromosome_len)
                chromosome = individual.chromosome.value
                var = "1" if chromosome[var_index] == "0" else "1"
                new_chromosome = chromosome[:var_index] + var + chromosome[var_index + 1:]
                individual.chromosome.value = new_chromosome
        self.calculate_fitness(pop)
        return pop

    def in_range(self, pop, p, p_select):
        for i in range(len(p_select)):
            if p_select[i][0] <= p <= p_select[i][1]:
                return pop[i]

    def init_pop(self, pop):
        self.calculate_fitness(pop)

    def evolution(self, pop, episode, variation_p):
        avgs = []
        episodes = []
        for e in range(episode):
            pop = self.selection(pop)
            pop = self.alternate(pop)
            pop = self.variation(pop, variation_p)
            avgs.append(self.fitness_avg(pop))
            episodes.append(e)
        return avgs, episodes


if __name__ == '__main__':
    POP_SIZE = 10
    EPISODE = 100
    VARIATION_P = 0.1
    ga = GA()
    pop = [Individual() for _ in range(POP_SIZE)]
    ga.init_pop(pop)
    avgs, episodes = ga.evolution(pop, EPISODE, VARIATION_P)
    acc = [7 * 7 * 3 for i in range(len(avgs))]

    plt.title('Result Analysis')
    plt.plot(episodes, acc, color='red', label="max fitness")
    plt.plot(episodes, avgs, color='blue', label="evolutionary algorithm")
    plt.legend(loc="best")
    plt.xlabel("episode")
    plt.ylabel("avg fitness")
    plt.savefig("result.png", dpi=100)
    plt.show()
