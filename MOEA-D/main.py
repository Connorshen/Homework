import numpy as np
import matplotlib.pyplot as plt


class Individual:

    def __init__(self, x):
        self.n_x = len(x)
        self.chromosome = Chromosome.encode(x)
        self.x = Chromosome.decode(self.chromosome)
        # 测试函数：https://blog.csdn.net/miscclp/article/details/38102831
        f1 = self.x[0]
        g = 1 + self.x[1]
        h = 1 - np.sqrt(f1 / g)
        f2 = g * h
        self.f = [f1, f2]


# 染色体
class Chromosome:
    # 编码成二进制字符串
    @staticmethod
    def encode(xs):
        res = []
        max_len = len(str(bin(10 ** 5)).replace("0b", ""))
        for x in xs:
            s = str(bin(int(x * (10 ** 5)))).replace("0b", "").zfill(max_len)
            res.append(s)
        return res

    # 解码成浮点数
    @staticmethod
    def decode(chromosomes):
        res = []
        for chromosome in chromosomes:
            res.append(int(chromosome, 2) / (10 ** 5))
        return res


class MOEAD:
    def __init__(self, n_pop, n_neighbor, episode):
        self.n_pop = n_pop
        self.n_neighbor = n_neighbor
        self.episode = episode

    # 交叉
    def crossover(self):
        pass

    # 变异
    def mutate(self):
        pass

    def best_value(self, pop):
        best = []
        nx = pop[0].n_x
        xs = []
        for individual in pop:
            xs.append(individual.x)
        xs = np.array(xs)
        for i in range(nx):
            x = xs[:, i]
            min = np.min(x)
            best.append(min)
        return best

    def neighbor(self, lamb, n_neighbor):
        b = []
        for i in range(len(lamb)):
            distances = []
            for j in range(len(lamb)):
                distance = np.sqrt(np.sum((np.array(lamb[i]) - np.array(lamb[j])) ** 2))
                distances.append(distance)
            neighbor_index = np.argsort(distances)
            b.append(neighbor_index[:n_neighbor])
        return b

    # 初始化
    def initial(self, n_pop):
        lamb = [[i / n_pop, 1 - i / n_pop] for i in range(n_pop)]
        pop = [Individual([np.random.random() for _ in range(2)]) for _ in range(n_pop)]
        return pop, lamb

    # 开始执行进化算法
    def evolve(self):
        pop, lamb = self.initial(n_pop=self.n_pop)
        b = self.neighbor(lamb=lamb, n_neighbor=self.n_neighbor)
        ep = []
        z = self.best_value(pop)
        print(1)


if __name__ == '__main__':
    N_POP = 100
    N_NEIGHBOR = 10
    EPISODE = 20

    moead = MOEAD(n_pop=N_POP, n_neighbor=N_NEIGHBOR, episode=EPISODE)
    moead.evolve()
