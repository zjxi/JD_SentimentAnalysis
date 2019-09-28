from snownlp import sentiment
import pandas as pd
import snownlp
import matplotlib.pyplot as plt
from matplotlib.font_manager import FontProperties
"""
    Written by Zijun Xi
    Date: 2019/9/28
"""


def read_csv():
    '''读取商品评论数据文件'''
    comment_data = pd.read_csv('comment_data.csv', encoding='gbk',
                               sep='\n', index_col=None)
    return comment_data


def clean_data(data):
    '''数据清洗'''
    df = data.dropna()  # 消除缺失数据 NaN为缺失数据
    df = pd.DataFrame(df.iloc[:, 0].unique())  # 数据去重
    return df
    # print('数据清洗后：', len(df))


def clean_repeat_word(raw_str, reverse=False):
    '''去除评论中的重复使用的词汇'''
    if reverse:
        raw_str = raw_str[::-1]
    res_str = ''
    for i in raw_str:
        if i not in res_str:
            res_str += i
    if reverse:
        res_str = res_str[::-1]
    return res_str


def processed_data(filename):
    '''清洗完毕的数据，并保存'''
    df = clean_data(read_csv())
    ser1 = df.iloc[:, 0].apply(clean_repeat_word)
    df2 = pd.DataFrame(ser1.apply(clean_repeat_word, reverse=True))
    df2.to_csv(f'{filename}.csv', encoding='gbk', index_label=None, index=None)


def train():
    '''训练正向和负向情感数据集，并保存训练模型'''
    sentiment.train('neg.txt', 'pos.txt')
    sentiment.save('sentiment.marshal')


sentiment_list = []

res_list = []


def test(filename, to_filename):
    '''商品评论-情感分析-测试'''
    with open(f'{filename}.csv', 'r', encoding='gbk') as fr:
        for line in fr.readlines():
            s = snownlp.SnowNLP(line)
            if s.sentiments > 0.6:
                res = '喜欢'
                res_list.append(1)
            elif s.sentiments < 0.4:
                res = '不喜欢'
                res_list.append(-1)
            else:
                res = '一般'
                res_list.append(0)
            sent_dict = {
                '情感分析结果': s.sentiments,
                '评价倾向': res,
                '商品评论': line
            }
            sentiment_list.append(sent_dict)
            print(sent_dict)
        df = pd.DataFrame(sentiment_list)
        df.to_csv(f'{to_filename}.csv', index=None, encoding='gbk',
                  index_label=None, mode='w')


def data_virtualization():
    '''分析结果可视化，以条形图为测试样例'''
    font = FontProperties(fname=r"C:\Windows\Fonts\simhei.ttf", size=14)
    likes = len([i for i in res_list if i == 1])
    common = len([i for i in res_list if i == 0])
    unlikes = len([i for i in res_list if i == -1])

    plt.bar([1], [likes], label='like')
    plt.bar([3], [common], label='common')
    plt.bar([5], [unlikes], label='unlike')

    plt.legend()
    plt.xlabel('result')
    plt.ylabel('value')
    plt.title(u'商品评论情感分析结果-条形图', FontProperties=font)
    plt.savefig('fig.png')
    plt.show()


def main():
    processed_data('processed_comment_data')
    # train()
    test('processed_comment_data', 'result')
    data_virtualization()


if __name__ == '__main__':
    main()



