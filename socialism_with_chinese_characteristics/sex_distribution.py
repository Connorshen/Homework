import sqlite3
import numpy as np
import matplotlib.pyplot as plt


def find_all_user():
    conn = sqlite3.connect("database/user_info.db")
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM user ")
    result = cursor.fetchall()
    cursor.close()
    conn.commit()
    conn.close()
    return result


if __name__ == '__main__':
    users = find_all_user()
    sex = [u[2] for u in users]
    man = np.array([p for p in sex if p == "男"])
    woman = np.array([p for p in sex if p == "女"])
    labels = '男', '女'
    fracs = [len(man) / len(sex), len(woman) / len(sex)]
    colors = ['tomato', 'lightskyblue']
    explode = [0, 0.1]
    plt.axes(aspect=1)
    plt.rcParams['font.sans-serif'] = ['SimHei']
    plt.pie(x=fracs, labels=labels, explode=explode, autopct='%3.1f %%',
            shadow=True, labeldistance=1.1, startangle=90, pctdistance=0.6, colors=colors)
    plt.legend(loc='upper right')
    plt.savefig("result_img/sex_distribution.png")
    plt.show()
