import numpy as np
import matplotlib.pyplot as plt

if __name__ == '__main__':
    x = np.sort(np.random.random(100) * 2 - 1)
    y1 = (x - 2) ** 2
    y2 = (x + 2) ** 2
    plt.plot(y1, y2)
    plt.show()
