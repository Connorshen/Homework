from store import PretreatMgr
import pandas as pd
import os.path
import re
import collections
import numpy as np
import jieba
import wordcloud
from PIL import Image
import matplotlib.pyplot as plt
import pylab


# 正则匹配删除
def regular(s_origin):
    result = [s_origin]
    useless = re.findall("(回复<a [^>]*?>.*?</a>:)", s_origin)
    useless.extend(re.findall("(<a [^>]*?>.*?</a>)", s_origin))
    useless.extend(re.findall("(<i [^>]*?>.*?</i>)", s_origin))
    for u in useless:
        result.append(result[-1].replace(u, ""))
    return result[-1]


def eachFile(need1, need2, filepath):
    pathDir = os.listdir(filepath)
    for allDir in pathDir:
        child = os.path.join('%s/%s' % (filepath, allDir))
        if os.path.isfile(child):
            a = []
            b = []
            data = PretreatMgr.restore(allDir[0:16])
            count = 0
            # 任意的多组列表
            for datas in data:
                for comments in datas:
                    a.append(regular(comments[need1]))
                    b_all.append(comments['user'][need2])
                    b.append(comments['user'][need2])
                    if count is 0:
                        for key in comments:
                            print(key)
                    count = count + 1
                # 字典中的key值即为csv中列名
                dataframe = pd.DataFrame({need1: a, need2: b})
                # 将DataFrame存储为csv,index表示是否显示行名，default=True
                dataframe.to_csv(
                    "csv/{filepath}/{weiboid}datas.csv".format(filepath=filepath[21:], weiboid=allDir[0:16]),
                    index=False, sep=',',
                    encoding='utf-8-sig')
            string_data = "".join(a)
            seg_list_exact = jieba.cut(string_data,
                                       cut_all=False)  # 精确模式分词
            object_list = []
            remove_words = [u'的', u'，', u'和', u'是', u'随着', u'对于', u'对', u'等', u'能', u'都', u'。', u' ', u'、', u'中', u'在',
                            u'了', u'通常', u'如果', u'我们', u'需要', u'[', u']', u'【', u'】', u'！', u'!', u'?', u'？']  # 自定义去除词库
            for word in seg_list_exact:  # 循环读出每个分词
                if word not in remove_words:  # 如果不在去除词库中
                    object_list.append(word)  # 分词追加到列表 # 词频统计
            word_counts = collections.Counter(object_list)  # 对分词做词频统计
            word_counts_top10 = word_counts.most_common(10)  # 获取前10最高频的词
            print(word_counts_top10)  # 输出检查
            #  词频展示
            mask = np.array(Image.open('yuntuback.png'))  # 定义词频背景
            wc = wordcloud.WordCloud(font_path='simhei.ttf', mask=mask, max_words=200,
                                     max_font_size=100, background_color="white")
            wc.generate_from_frequencies(word_counts)  # 从字典生成词云
            image_colors = wordcloud.ImageColorGenerator(mask)  # 从背景图建立颜色方案
            wc.recolor(color_func=image_colors)  # 将词云颜色设置为背景图方案
            plt.imshow(wc)  # 显示词云 plt.axis('off') # 关闭坐标轴 plt.show() # 显示图像
            plt.axis("off")
            plt.savefig(os.path.join('%s/%s/%s.jpg' % ("WordCloud", filepath[21:], allDir[0:16])), dpi=300)
            # pylab.show()
            print()
            #             print child.decode('gbk') # .decode('gbk')是解决中文显示乱码问题
            continue
    PretreatMgr.save_file("weibo_users", "user_ids", b_all)


if __name__ == '__main__':
    b_all = []
    eachFile("text", "id", "completed_weibo_data/中国国际进口博览会")
    eachFile("text", "id", "completed_weibo_data/十九大")
    eachFile("text", "id", "completed_weibo_data/世界互联网大会")
