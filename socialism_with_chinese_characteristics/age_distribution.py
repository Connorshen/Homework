import sqlite3
import numpy as np
import pandas as pd
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
    birthdays = [u[4].split("-") for u in users if
                 u[4] != "None" and len(u[4]) == 10 and 1918 < int(u[4].split("-")[0]) < 2008]
    ages = np.array([2018 - int(b[0]) for b in birthdays if 1 <= 2018 - int(b[0]) <= 79])
    df = pd.DataFrame(np.zeros(8), index=["0-9", "10-19", "20-29", "30-39", "40-49", "50-59", "60-69", "70-79"],
                      columns=["人数"])
    for age in ages:
        p = int(age / 10)
        df.iloc[p]["人数"] += 10
    print(df)

    y_list = df.index.tolist()
    p_nums = df.loc[:, "人数"]
    plt.rcParams['font.sans-serif'] = ['SimHei']
    plt.barh(range(len(p_nums)), p_nums, tick_label=y_list, fc='deepskyblue')
    plt.xlabel("人数")
    plt.ylabel("年龄")
    plt.savefig("result_img/age_distribution.png")
    plt.show()
