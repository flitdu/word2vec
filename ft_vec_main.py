# -*- coding: utf-8 -*-
"""
Created by Dufy on 2020/2/26  14:30
IDE used: PyCharm 
Description :fasttext 词向量
1)# 原文链接：https://blog.csdn.net/sinat_26917383/article/details/83041424
《极简使用︱Gensim-FastText 词向量训练以及OOV（out-of-word）问题有效解决》
2)
Remark:      
"""
import fasttext
from gensim.models import FastText
from gensim.test.utils import datapath
from FTvec_data_read import excel_read2txt
from jieba_pos import PN_if
import jieba.posseg as pseg
from data_operation.function import load_stop_word_list, label_new, fast_vec_standard
stop_words = load_stop_word_list("stopwords_subclass.txt")


def train_model_gensim():
    pass
    corpus_files = datapath(r'D:\dufy\code\fasttext_vec\data\txt_file\corpus.txt')  #加载语料

    # model = FastText(corpus_file=corpus_files, size=100, window=5, min_count=2, iter=10, min_n=1, max_n=20, word_ngrams=1)
    model = FastText(corpus_file=corpus_files)

    model.save(r'D:\dufy\code\ft_BOM\model_vec\gensim_vec.bin')    # 模型保存

    print('gensim 训练结束....')

def train_model_ft():
    pass
    model = fasttext.train_unsupervised(r'D:\dufy\code\ft_BOM\data\ft_vec\txt_file\corpus_v1.txt',
                                        epoch=5,  #5
                                        loss='ns',  # 采用 softmax 速度会很慢！！！
                                        lr=0.05,
                                        wordNgrams=2,
                                        minCount=1,  # 词频阈值, 小于该值在初始化时会过滤掉
                                        minn=3,     #  1
                                        maxn=10)
    # model.save_model(r'.\model\ft_vec.bin')
    model.save_model(r'D:\dufy\code\ft_BOM\model_vec\ft_vec_v1.bin')  # 版本号
    print('fasttext 训练结束....')


if __name__ == "__main__":
    pass
    # excel_read2txt()

    tag = 1

    if tag == 1:
        train_model_ft()

        model = fasttext.load_model(r'D:\dufy\code\ft_BOM\model_vec\ft_vec_v1.bin')

        print(model.get_word_vector('3v'))
        print(model.words)

        print(model.get_nearest_neighbors('0402B104K160CT'.lower()))
        print(model.get_nearest_neighbors('0402B104K160Cj'.lower()))

        print(model.get_nearest_neighbors('0402B104K160-xxxxxxx'.lower()))
        print(model.get_nearest_neighbors('50v-0402B104K160-xxxxxxx'.lower()))
        print(model.get_nearest_neighbors('1.CP.0402000012PKA'.lower()))
        print(model.get_nearest_neighbors('262ly221k'.lower()))
        print(model.get_nearest_neighbors('50 v'.lower()))
        print(model.get_nearest_neighbors('50v'.lower()))

        while True:
            bom_line = input('输入待预测BOM行：')
            aa_description = " ".join(bom_line.split()[0:])
            aa_description = fast_vec_standard(aa_description, stop_words)  # 标准化处理
            print(aa_description)
            if bom_line != 'end':
                # for i in aa_description.split():
                for _, i in enumerate(aa_description.split()):
                    print(i, ':')
                    pn_tag = []
                    for j in model.get_nearest_neighbors(i.lower()):
                        pn_judge = PN_if(j[1])
                        pn_tag.append(pn_judge)
                    print(pn_tag)
                    p_k = 0
                    for index, j in enumerate(model.get_nearest_neighbors(i.lower())):
                        if pn_tag[index] == 1:
                            pass
                            print('{} ：\033[1;31m {}\033[0m'.format(j, pn_tag[index]))  # 显示红色
                        else:
                            print('{} ：\033[1;32m {}\033[0m'.format(j, pn_tag[index]))
                        p_k += pn_tag[index] * j[0]
                    print('\033[1;32m 置信概率：{}\033[0m'.format(p_k/10))
                    print('\n ==============================')
                # line_txt_list = []
                # words1 = pseg.cut(bom_line)
                # # words2 = pseg.cut(bom_line.replace('-', ''))
                # for word, flag in words1:
                #     line_txt_list.append('%s %s' % (word, flag))
                # # for word, flag in words2:
                # #     line_txt_list.append('%s %s' % (word, flag))
                # list_new = list(set(line_txt_list))
                # print('|'.join(list_new))
            else:
                break  # 结束循环

        pass
    # 2： gensim 训练
    if tag == 2:

        # train_model_gensim()

        model_ft_vec = FastText.load(r'D:\dufy\code\ft_BOM\model_vec\gensim_vec.bin')  # ==========获取词向量

    #     # 判断是否在词库：
    #     print('你' in model_ft_vec.wv.vocab)
    #     print('美元' in model_ft_vec.wv.vocab)
    #
    #     # print(model['你'])  # 词向量获得的方式
    #     print('\033[1;32m {}\033[0m'.format(model_ft_vec.wv['你']))
    #
    #
    # # ============求相似
        print('0402b104k160cj' in model_ft_vec.wv.vocab)
        print('0402b104k160ct' in model_ft_vec.wv.vocab)
        print(model_ft_vec.wv.similarity('0402b104k160cj', '0402b104k160ct'), '\n ------')  # 求相似
        print(model_ft_vec.wv.similarity('0402b104k160ct', '0402b104k160cj'),'\n ------')  # 求相似
    #     print(model_ft_vec.wv.n_similarity(['cat', 'say'], ['dog', 'say']))  # 多个词条求相似,为求多个词之间的相似性
        print(model_ft_vec.wv.most_similar("0402b104k160cj".lower()),'\n ------')   # 0402b104k160ct
        print(model_ft_vec.wv.most_similar("0402B104K160ct".lower()),'\n ------')
        print(model_ft_vec.wv.most_similar("50 v".lower()),'\n ------')


