import numpy as np
import matplotlib.pyplot as plt


class Individual:
    pass


class MOEAD:
    def __init__(self, n_pop, n_neighbor):
        pass

    # 开始执行进化算法
    def evolve(self):
        pass

    # 交叉
    def crossover(self):
        pass

    # 变异
    def mutate(self):
        pass


if __name__ == '__main__':
    x = np.sort(np.random.random(100) * 2 - 1)
    y1 = (x - 2) ** 2
    y2 = (x + 2) ** 2
    plt.plot(y1, y2)
    plt.show()
