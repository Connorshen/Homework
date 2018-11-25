import numpy as np
import matplotlib.pyplot as plt

if __name__ == '__main__':
    x = np.sort(np.random.random(1000) * 8 - 5)
    y1 = x ** 2
    y2 = (x + 2) ** 2
    plt.plot(x, y1, label="y=x^2")
    plt.plot(x, y2, label="y=(x+2)^2")
    plt.legend(loc="best")
    plt.savefig("mop.png", dpi=100)
    plt.show()
