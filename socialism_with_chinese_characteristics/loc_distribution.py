import sqlite3
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
from mpl_toolkits.basemap import Basemap
from matplotlib.patches import Polygon
from matplotlib.colors import rgb2hex


# 地理位置分布
# vmin最小人数，vmax最大人数
def paint(data, vmin=1, vmax=100):
    plt.figure(figsize=(8, 8))
    map = Basemap(
        llcrnrlon=77,
        llcrnrlat=14,
        urcrnrlon=140,
        urcrnrlat=51,
        projection='lcc',
        lat_1=33,
        lat_2=45,
        lon_0=100
    )
    map.drawcountries(linewidth=1.5)
    map.drawcoastlines()
    map.readshapefile('map_info/gadm36_CHN_1', 'states', drawbounds=True)

    provinces = map.states_info
    statenames = []
    colors = {}
    cmap = plt.cm.YlOrRd

    for each_province in provinces:
        province_name = each_province['NL_NAME_1']
        p = province_name.split('|')
        if len(p) > 1:
            s = p[1]
        else:
            s = p[0]
        s = s[:2]
        if s == '黑龍':
            s = '黑龙江'
        if s == '内蒙':
            s = '内蒙古'
        statenames.append(s)
        if s in data.index.tolist():
            pop = data.loc[s]['人数']
        else:
            pop = 0
        colors[s] = cmap(np.sqrt((pop - vmin) / (vmax - vmin)))[:3]
    ax = plt.gca()
    for nshape, seg in enumerate(map.states):
        color = rgb2hex(colors[statenames[nshape]])
        poly = Polygon(seg, facecolor=color, edgecolor=color)
        ax.add_patch(poly)
    plt.savefig("result_img/loc_distribution.png")
    plt.show()


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
    locs = np.array([u[3].split(" ")[0] for u in users if u[3] != "其他" and u[3] != "海外"])
    df = pd.DataFrame(columns=['人数'])
    for loc in locs:
        if loc in df.index.tolist():
            df.loc[loc]['人数'] += 1
        else:
            df.loc[loc] = 1
    df.sort_values(by=['人数'], inplace=True, ascending=False)
    print(df)
    paint(df, vmin=1, vmax=100)
