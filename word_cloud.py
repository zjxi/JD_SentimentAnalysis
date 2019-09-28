from wordcloud import WordCloud
import jieba
import matplotlib.pyplot as plt
"""
    Written by Zijun Xi
    Date: 2019/9/28
"""


def word_cloud_creation(filename):
    '''创建词云，并进行分词'''
    text = open(filename).read()
    word_list = jieba.cut(text, cut_all=True)
    wl = ' '.join(word_list)
    return wl


def word_cloud_settings():
    '''设置词云的属性'''
    wc = WordCloud(
        background_color='white',
        max_words=2000,
        max_font_size=100,
        height=1200,
        width=1500,
        random_state=30,
        font_path='C:\Windows\Fonts\simfang.ttf'
    )
    return wc


def word_cloud_implementation(wl, wc):
    '''生成词云，并展示'''
    my_words = wc.generate(wl)
    plt.imshow(my_words)
    plt.axis('off')
    wc.to_file(f'./assets/word_cloud.png')
    plt.show()
